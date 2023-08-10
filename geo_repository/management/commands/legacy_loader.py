import json
from datetime import datetime

import psycopg2
from geo_repository.models import ZMR, ZMRGeometry


class Zone:
    def __init__(self, id, name, geom, lpu=None, db=None, unique_id=None):
        self.id = id
        self.name = name
        self.geom = geom
        self.lpu = lpu
        self.db = db
        self.unique_id = unique_id

    def make_unique_id(self):
        return f'{self.id}_{self.lpu}_{self.db}_{self.name}'

    def __str__(self):
        return f'{self.name}[{self.id}]'

    def __repr__(self):
        return self.__str__()


class ViolObject:
    def __init__(self, id, object_type, object_subtype1, object_subtype2, geom, lpu=None, db=None):
        self.id = id
        self.object_type = object_type
        self.object_subtype1 = object_subtype1
        self.object_subtype2 = object_subtype2
        self.geom = geom
        self.lpu = lpu
        self.db = db

    def __str__(self):
        return f'{self.db}_{self.lpu}_{self.object_type}-{self.object_subtype1}-{self.object_subtype2} [{self.id}]'

    def __repr__(self):
        return self.__str__()


class LegacyDB:
    def __init__(self, db_name='transgaz_chaykovskiy'):
        self.host = 'localhost'
        self.port = 5432
        self.dbname = db_name
        self.user = 'postgres'
        self.password = '12345'

        self.conn = self.connect()
        self.cursor = self.get_cursor()

        self.lpu_names = self.get_lpu_names()

    def connect(self):
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password
        )

    def get_cursor(self):
        return self.conn.cursor()

    def execute(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_lpu_names(self):
        lpus = self.execute("SELECT schema_name FROM information_schema.schemata")
        return [lp[0] for lp in lpus[:3]]

    def get_latest_zmr_table(self, schema, date=None):
        condition = f"AND table_name LIKE 'ZMR_all_{date}'" if date else "AND table_name LIKE 'ZMR_all_%'"
        zmr_table = self.execute(
            f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}' {condition} ORDER BY table_name DESC")
        if zmr_table:
            return zmr_table[0][0]

    def get_latest_object_table(self, schema, date=None):
        condition = f"AND table_name LIKE 'air_objects__{date}'" if date else "AND table_name LIKE 'airp_objects__%' " \
                                                                              "AND table_name NOT LIKE '%_notselected'"
        object_table = self.execute(
            f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}' {condition} ORDER BY table_name DESC")
        if object_table:
            return object_table[0][0]

    def get_zones(self):
        zones = []
        for schema in self.lpu_names:
            zmr_table = self.get_latest_zmr_table(schema)
            if zmr_table:
                zmr = self.execute(f'SELECT id, name, geom FROM {schema}."{zmr_table}" WHERE geom IS NOT NULL')
                zones.extend([Zone(id=z[0], name=z[1], geom=z[2], lpu=schema, db=self.dbname) for z in zmr])
        return zones

    def get_objects(self):
        objects = []
        for schema in self.lpu_names:
            object_table = self.get_latest_object_table(schema)
            if object_table:
                viol_objects = self.execute(
                    f'SELECT id, type, podtype, geomorf, geom FROM {schema}."{object_table}" '
                    f'WHERE geom IS NOT NULL AND type IS NOT NULL AND podtype IS NOT NULL AND geomorf IS NOT NULL')
                objects.extend([ViolObject(id=o[0], object_type=o[1], object_subtype1=o[2], object_subtype2=o[3],
                                           geom=o[4], lpu=schema, db=self.dbname) for o in viol_objects])
        return objects

    def close(self):
        self.cursor.close()
        self.conn.close()


class ZonesManager:
    def __init__(self, objects):
        self.legacy_zmr = objects
        self.zones_relations_file = 'zones_relations.json'
        self.zones_relations = []
        self.load_zones_relations()

    def load_zones_relations(self):
        self.save_all_to_django()

        # if pathlib.Path(self.zones_relations_file).exists():
        #     with open(self.zones_relations_file, 'r') as f:
        #         self.zones_relations = json.load(f)
        #         self.check_zones_relations()
        # else:
        #     self.save_all_to_django()

    def check_zones_relations(self):
        for legacy_zmr in self.legacy_zmr:
            found_in_django = False

            for relation in self.zones_relations:
                if legacy_zmr.make_unique_id() == relation['unique_id']:
                    found_in_django = True

                    if legacy_zmr.geom != relation['geom']:
                        self.update_zone(legacy_zmr)
                        relation['geom'] = legacy_zmr.geom
                    break

            if not found_in_django:
                self.create_zone(legacy_zmr)

        for relation in self.zones_relations[:]:
            found_in_legacy = any(
                legacy_zmr.make_unique_id() == relation['unique_id'] for legacy_zmr in self.legacy_zmr)
            if not found_in_legacy:
                self.delete_zone_by_relation(relation)

        self.save_to_file(self.zones_relations)

    @staticmethod
    def update_zone(legacy_zmr):
        zone = ZMR.objects.get(unique_id=legacy_zmr.make_unique_id())
        zone_geometry = ZMRGeometry.objects.get(zone=zone)

        zone_geometry.is_relevant = False
        zone_geometry.date_end = datetime.now()
        zone_geometry.save()

        ZMRGeometry.objects.create(zone=zone, geom=legacy_zmr.geom)

    def create_zone(self, legacy_zmr):
        new_zone = ZMR(name=legacy_zmr.name, unique_id=legacy_zmr.make_unique_id())
        new_zone.save()

        zone_geometry = ZMRGeometry(zone=new_zone, geom=legacy_zmr.geom)
        zone_geometry.save()

        self.zones_relations.append(self.make_relation(unique_id=legacy_zmr.make_unique_id(), geom=legacy_zmr.geom))

    def delete_zone_by_relation(self, relation):
        django_zone = ZMR.objects.get(unique_id=relation['unique_id'])
        django_zone.delete()

        zone_geometry = ZMRGeometry.objects.filter(zone=django_zone)
        for z in zone_geometry:
            z.delete()

        self.zones_relations.remove(relation)

    def save_all_to_django(self):
        ZMR.objects.all().delete()
        ZMRGeometry.objects.all().delete()

        zones = []
        zones_geometries = []
        relations = []

        for zmr in self.legacy_zmr:
            zone = ZMR(name=zmr.name)  # unique_id=zmr.make_unique_id())
            zones.append(zone)

            zone_geometry = ZMRGeometry(zone=zone, geom=zmr.geom)
            zones_geometries.append(zone_geometry)

            # relations.append(self.make_relation(unique_id=zmr.make_unique_id(), geom=zmr.geom))

        ZMR.objects.bulk_create(zones)
        ZMRGeometry.objects.bulk_create(zones_geometries)
        # self.save_to_file(relations)

    @staticmethod
    def make_relation(unique_id, geom):
        return {
            'unique_id': unique_id,
            'geom': geom,
        }

    def save_to_file(self, data):
        with open(self.zones_relations_file, 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


class ObjectsManager:
    def __init__(self, objects):
        self.objects = objects
        self.load_objects_relations()

    def load_objects_relations(self):
        self.save_all_to_django()

    def save_all_to_django(self):
        Object.objects.all().delete()
        ObjectGeometry.objects.all().delete()

        viol_objects = []
        objects_geometries = []

        for obj in self.objects:
            object_type = ObjectType.objects.filter(value=obj.object_type).first()
            object_subtype1 = ObjectSubType1.objects.filter(value=obj.object_subtype1,
                                                            object_type=object_type).first()
            object_subtype2 = ObjectSubType2.objects.filter(value=obj.object_subtype2,
                                                            object_subtype1=object_subtype1).first()

            viol_object = Object(name='Объект нарушения',
                                 object_type=object_type,
                                 object_subtype1=object_subtype1,
                                 object_subtype2=object_subtype2,
                                 fill_style='#000000FF',
                                 border_style='#000000FF',
                                 border_width=3, )
            viol_objects.append(viol_object)

            object_geometry = ObjectGeometry(object=viol_object, geom=obj.geom)
            objects_geometries.append(object_geometry)

        Object.objects.bulk_create(viol_objects)
        ObjectGeometry.objects.bulk_create(objects_geometries)


db_list = ['transgaz_samara', 'gazprom_dobycha_krasnodar', 'gazprom_pererabotka', 'transgaz_chaykovskiy',
           'transgaz_chechen', 'transgaz_ekaterenburg', 'transgaz_kazan', 'transgaz_krasnodar', 'transgaz_mahachkala',
           'transgaz_moskva', 'transgaz_nizhniy_novgorod', 'transgaz_saratov', 'transgaz_spb', 'transgaz_stavropol',
           'transgaz_surgut', 'transgaz_tomsk', 'transgaz_tomsk_silasibiri', 'transgaz_ufa', 'transgaz_ugorsk',
           'transgaz_uhta', 'transgaz_volgograd']


def load_zones():
    start_time = datetime.now()

    zones = []

    for db in db_list[:1]:
        legacy_db = LegacyDB(db_name=db)
        zones.extend(legacy_db.get_zones())
        legacy_db.close()

    print(f'Получено {len(zones)} зон. Запуск проверки и загрузки в БД Django')
    ZonesManager(zones)

    end_time = datetime.now()
    print(f'Загрузка завершена за {end_time - start_time}')


def load_objects():
    start_time = datetime.now()

    objects = []

    for db in db_list[:1]:
        legacy_db = LegacyDB(db_name=db)
        objects.extend(legacy_db.get_objects())
        legacy_db.close()

    print(f'Получено {len(objects)} объектов нарушений. Запуск проверки и загрузки в БД Django')
    ObjectsManager(objects)

    end_time = datetime.now()
    print(f'Загрузка завершена за {end_time - start_time}')
