from django.contrib.gis.geos import GeometryCollection, GEOSGeometry
import psycopg2
from geo_repository.models import ZMR, ZMRGeometry, OZ, OZGeometry, ProtectedObject, ProtectedObjectGeometry
from datetime import datetime
from django.db.models import Q


class OZObject:
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


class ZoneObject:
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


class ProtectedObjectObject:
    def __init__(self, id, name, geom, lpu=None, db=None, unique_id=None):
        self.id = id
        self.name = name
        self.geom = GEOSGeometry(geom)
        self.lpu = lpu
        self.db = db
        self.unique_id = unique_id

    def union_geometry(self, geom):
        new_geom = GEOSGeometry(geom)
        self.geom = self.geom.union(new_geom)

    def make_unique_id(self):
        return f'{self.id}_{self.lpu}_{self.db}_{self.name}'

    def __str__(self):
        return f'{self.name}[{self.id}]'

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
        lpus = self.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name LIKE '%_lpu'")
        return [lp[0] for lp in lpus[:1]]

    def get_latest_zmr_table(self, schema, date=None):
        condition = f"AND table_name LIKE 'ZMR_all_{date}'" if date else "AND table_name LIKE 'ZMR_all_%'"
        zmr_table = self.execute(
            f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema}' {condition} ORDER BY table_name DESC")
        if zmr_table:
            return zmr_table[0][0]

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
                zones.extend([ZoneObject(id=z[0], name=z[1], geom=z[2], lpu=schema, db=self.dbname) for z in zmr])
        return zones

    def get_oz(self):
        oz = []
        for schema in self.lpu_names:
            oz_table = self.get_latest_oz_table(schema)
            if oz_table:
                oz_objects = self.execute(
                    f'SELECT id, name, geom FROM {schema}."{oz_table}" WHERE geom IS NOT NULL')
                oz.extend([OZObject(id=o[0], name=o[1], geom=o[2], lpu=schema, db=self.dbname) for o in oz_objects])
        return oz

    def get_protected_objects(self):
        protected_objects = []
        for schema in self.lpu_names:
            all_protected_objects = self.execute(f'SELECT id, name, geom, lpu FROM "public"."tubes_tg" WHERE end_date IS NULL AND geom IS NOT NULL AND lpu = \'{schema}\' ORDER BY id')
            for pr_object in all_protected_objects:
                if pr_object[1] in [po.name for po in protected_objects]:
                    for po in protected_objects:
                        if po.name == pr_object[1]:
                            po.union_geometry(pr_object[2])
                else:
                    protected_objects.append(ProtectedObjectObject(id=pr_object[0], name=pr_object[1], geom=pr_object[2], db=self.dbname, lpu=pr_object[3]))
        return protected_objects

    def close(self):
        self.cursor.close()
        self.conn.close()


class ProtectedObjectManager:
    def __init__(self, objects):
        self.legacy_pr_obj = objects
        self.save_all_to_django()

    def save_all_to_django(self):
        ProtectedObject.objects.all().delete()
        ProtectedObjectGeometry.objects.all().delete()

        protected_objects = []
        protected_object_geometries = []

        for pr_object in self.legacy_pr_obj:
            new_pr_object = ProtectedObject(name=pr_object.name)
            protected_objects.append(new_pr_object)
            new_geom_object = ProtectedObjectGeometry(parent_object=new_pr_object, geom=GeometryCollection(pr_object.geom))
            protected_object_geometries.append(new_geom_object)

        ProtectedObject.objects.bulk_create(protected_objects)
        ProtectedObjectGeometry.objects.bulk_create(protected_object_geometries)


class ZoneManager:
    def __init__(self, zones):
        self.legacy_zones = zones
        self.save_all_to_django()

    def save_all_to_django(self):
        ZMR.objects.all().delete()
        ZMRGeometry.objects.all().delete()

        zmr_objects = []
        zmr_geometries = []

        for zone in self.legacy_zones:
            protected_object = ProtectedObject.objects.filter(
                Q(protected_object_geometry__geom__intersects=zone.geom) &
                Q(name=zone.name)
            ).first()
            new_zmr_object = ZMR(protected_object=protected_object, name=zone.name)
            zmr_objects.append(new_zmr_object)

            new_geom_object = ZMRGeometry(parent_object=new_zmr_object, geom=zone.geom)
            zmr_geometries.append(new_geom_object)

        ZMR.objects.bulk_create(zmr_objects)
        ZMRGeometry.objects.bulk_create(zmr_geometries)


class OZManager:
    def __init__(self, oz):
        self.legacy_oz = oz
        self.save_all_to_django()

    def save_all_to_django(self):
        OZ.objects.all().delete()
        OZGeometry.objects.all().delete()

        oz_objects = []
        oz_geometries = []

        for oz in self.legacy_oz:
            protected_object = ProtectedObject.objects.filter(
                Q(protected_object_geometry__geom__intersects=oz.geom) &
                Q(name=oz.name)
            ).first()

            new_oz_object = OZ(protected_object=protected_object, name=oz.name)
            oz_objects.append(new_oz_object)

            new_geom_object = OZGeometry(parent_object=new_oz_object, geom=oz.geom)
            oz_geometries.append(new_geom_object)

        OZ.objects.bulk_create(oz_objects)
        OZGeometry.objects.bulk_create(oz_geometries)


db_list = ['transgaz_samara', 'gazprom_dobycha_krasnodar', 'gazprom_pererabotka', 'transgaz_chaykovskiy',
           'transgaz_chechen', 'transgaz_ekaterenburg', 'transgaz_kazan', 'transgaz_krasnodar', 'transgaz_mahachkala',
           'transgaz_moskva', 'transgaz_nizhniy_novgorod', 'transgaz_saratov', 'transgaz_spb', 'transgaz_stavropol',
           'transgaz_surgut', 'transgaz_tomsk', 'transgaz_tomsk_silasibiri', 'transgaz_ufa', 'transgaz_ugorsk',
           'transgaz_uhta', 'transgaz_volgograd']


def load_protected():
    start_time = datetime.now()

    pr_objects = []

    for db in db_list[:1]:
        legacy_db = LegacyDB(db_name=db)
        pr_objects.extend(legacy_db.get_protected_objects())
        legacy_db.close()

    print(f'Получено {len(pr_objects)} охраняемых объектов. Запуск проверки и загрузки в БД Django')
    ProtectedObjectManager(pr_objects)

    end_time = datetime.now()
    print(f'Загрузка завершена за {end_time - start_time}')


def load_zones():
    start_time = datetime.now()

    zones = []

    for db in db_list[:1]:
        legacy_db = LegacyDB(db_name=db)
        zones.extend(legacy_db.get_zones())
        legacy_db.close()

    print(f'Получено {len(zones)} зон минимальных расстояний. Запуск проверки и загрузки в БД Django')
    ZoneManager(zones)

    end_time = datetime.now()
    print(f'Загрузка завершена за {end_time - start_time}')


def load_oz():
    start_time = datetime.now()

    oz = []

    for db in db_list[:1]:
        legacy_db = LegacyDB(db_name=db)
        oz.extend(legacy_db.get_oz())
        legacy_db.close()

    print(f'Получено {len(oz)} охранных зон. Запуск проверки и загрузки в БД Django')
    OZManager(oz)

    end_time = datetime.now()
    print(f'Загрузка завершена за {end_time - start_time}')
