import json
from datetime import datetime

import psycopg2
from geo_repository.models import ZMR, ZMRGeometry, OZ, OZGeometry


class OZ_Object:
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

    def get_latest_oz_table(self, schema, date=None):
        condition = f"AND table_name LIKE 'OZ_all_{date}'" if date else "AND table_name LIKE 'OZ_all_%'"
        oz_table = self.execute(
            f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}' {condition} ORDER BY table_name DESC")
        if oz_table:
            return oz_table[0][0]

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

    def get_oz(self):
        oz = []
        for schema in self.lpu_names:
            oz_table = self.get_latest_oz_table(schema)
            if oz_table:
                oz_objects = self.execute(
                    f'SELECT id, name, geom FROM {schema}."{oz_table}" WHERE geom IS NOT NULL')
                oz.extend([OZ_Object(id=o[0], name=o[1], geom=o[2], lpu=schema, db=self.dbname) for o in oz_objects])
        return oz

    def close(self):
        self.cursor.close()
        self.conn.close()


class ZonesManager:
    def __init__(self, objects):
        self.legacy_zmr = objects
        self.save_all_to_django()

    def save_all_to_django(self):
        ZMR.objects.all().delete()
        ZMRGeometry.objects.all().delete()

        zones = []
        zones_geometries = []

        for zmr in self.legacy_zmr:
            zone = ZMR(name=zmr.name)
            zones.append(zone)

            zone_geometry = ZMRGeometry(zone=zone, geom=zmr.geom)
            zones_geometries.append(zone_geometry)

        ZMR.objects.bulk_create(zones)
        ZMRGeometry.objects.bulk_create(zones_geometries)


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


class OZManager:
    def __init__(self, objects):
        self.legacy_oz = objects
        self.save_all_to_django()

    def save_all_to_django(self):
        OZ.objects.all().delete()
        OZGeometry.objects.all().delete()

        oz = []
        oz_geometries = []

        for oz_obj in self.legacy_oz:
            zone = OZ(name=oz_obj.name)
            oz.append(zone)

            zone_geometry = OZGeometry(zone=zone, geom=oz_obj.geom)
            oz_geometries.append(zone_geometry)

        OZ.objects.bulk_create(oz)
        OZGeometry.objects.bulk_create(oz_geometries)


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


def load_oz():
    start_time = datetime.now()

    ozs = []

    for db in db_list[:1]:
        legacy_db = LegacyDB(db_name=db)
        ozs.extend(legacy_db.get_oz())
        legacy_db.close()

    print(f'Получено {len(ozs)} охранных зон. Запуск проверки и загрузки в БД Django')
    OZManager(ozs)

    end_time = datetime.now()
    print(f'Загрузка завершена за {end_time - start_time}')
