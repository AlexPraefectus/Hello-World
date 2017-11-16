from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker


class REGION:
    def __init__(self, params):
        self.name = params[0]
        self.population = params[1]
        self.square = params[2]
        self.city_list = params[3]

    def __repr__(self):
        return 'Name: {}\n' \
               'Population: {}\n' \
               'Square: {}\n' \
               'Big cities: {}\n'.format(self.name, self.population, self.square, ',  '.join(self.city_list))

    def belonging(self, city_to_find):
        if city_to_find in self.city_list:
            return True
        else:
            return False

    def population_density(self):
        return float('{.2f}'.format(self.population / self.square))


# database declaration
Base = declarative_base()
engine = create_engine('mysql+pymysql://lab_6:lab_6@localhost:3306/lab_6', pool_recycle=3600, encoding='utf8')
Session = sessionmaker(bind=engine)
session = Session()


class Region(Base):
    __tablename__ = 'regions'
    region_id = Column(Integer(), primary_key=True)
    region_name = Column(String(50), nullable=False)
    region_population = Column(Integer(), nullable=False)
    region_square = Column(Integer, nullable=False)


class City(Base):
    __tablename__ = 'cities'
    city_id = Column(Integer(), primary_key=True)
    city_name = Column(String(20), nullable=False)
    region_id = Column(Integer(), ForeignKey('regions.region_id'), nullable=False)
    region = relationship('Region', backref=backref('regions'), order_by=city_id)


class DBCONTROLLERS:
    @staticmethod
    def add_region():
        """
        adding new record(new region) to 'regions' and new record to 'cities' table linked to previously added region
        """
        while True:
            try:
                region_name = input('Type region name: ')
                population = int(input('Type region population: '))
                assert population > 0, 'population can not be non-positive number'
                square = int(input('Type region square: '))
                assert square > 0, 'square can not be non-positive number'
                new_region = Region(region_name=region_name,
                                    region_population=population,
                                    region_square=square)
                session.add(new_region)
                session.commit()
                reg_id = session.query(Region.region_name, Region.region_id).filter(
                    Region.region_name == region_name).first()
                reg_id = reg_id.region_id
                while True:
                    a = input('Type name of a city (\'stop\' to stop')
                    if a == 'stop':
                        break
                    else:
                        new_city = City(city_name=a,
                                        region_id=reg_id)
                        session.add(new_city)
                        session.commit()
                print('Region \'{}\' added'.format(region_name))
            except AssertionError:
                print('Your data seems to be not real, try again.'
                      ' Remember that population and square should be more than 0')
            except ValueError:
                print('Your input is incorrect, try again')
            break
        return

    @staticmethod
    def add_city():
        print('Regions:')
        tmp_regions = session.query(Region).all()
        for i in tmp_regions:
            print("{}. {}".format(i.region_id, i.region_name))
        try:
            chosen_region = int(input('Choose a region to add a city (type number of chosen region) '))
            assert chosen_region in [j.region_id for j in tmp_regions], 'id does not exist'
            new_city_name = input('Type name of the city ')
            reg_id = session.query(Region).filter(Region.region_id == chosen_region).first().region_id
            new_city = City(city_name=new_city_name,
                            region_id=reg_id)
            session.add(new_city)
            session.commit()
            print('Adding city succeeded')
        except ValueError:
            print('input data can not be interpreted as number')
        except AssertionError:
            print('Chosen number of region does not exist in table')
        return

    @staticmethod
    def edit_region():
        tmp_regions = session.query(Region.region_id, Region.region_name).all()
        for i in tmp_regions:
            print('{}. {}'.format(i.region_id, i.region_name))
        try:
            chosen_reg_id = int(input('Choose a region to edit (Type its number) '))
            assert chosen_reg_id in [j.region_id for j in tmp_regions], 'id does not exist'
            chosen_reg = session.query(Region).filter(Region.region_id == chosen_reg_id).first()
            new_name = input('Type new name for this region ')
            new_population = int(input('Type new population for this region '))
            assert new_population > 0, 'population can not be non-positive number'
            new_square = int(input('Type new square for this region '))
            assert new_square > 0, 'square can not be non-positive number'
            chosen_reg.region_name = new_name
            chosen_reg.region_population = new_population
            chosen_reg.region_square = new_square
            session.commit()
            choice = int(input('Do u want to add new cities? (1/0) '))
            if choice:
                while True:
                    a = input('Type name of a city (\'stop\' to stop')
                    if a == 'stop':
                        break
                    else:
                        new_city = City(city_name=a,
                                        region_id=chosen_reg_id)
                        session.add(new_city)
                        session.commit()
            print('Edit succeeded')
        except AssertionError:
            print('Your data seems to be not real, try again.'
                  ' Remember that population and square should be more than 0 ')
        except ValueError:
            print('Your input is incorrect')

    @staticmethod
    def edit_city():
        tmp_cities = session.query(City.city_id, City.city_name).all()
        for i in tmp_cities:
            print('{}. {}'.format(i.city_id, i.city_name))
        try:
            chosen_city = int(input('Type number of chosen city '))
            assert chosen_city in [j.city_id for j in tmp_cities], 'id does not exist'
            edited_city = session.query(City).filter(City.city_id == chosen_city).first()
            new_name = input('Type new name for this city ')
            choice = int(input('Do you want to choose another region for this city? (1/0) '))
            if choice:
                tmp_regions = session.query(Region.region_id, Region.region_name).all()
                print(['{}. {}'.format(j.region_id, j.region_name) for j in tmp_regions])
                chosen_region = int(input('Type number of chosen region'))
                assert chosen_region in [j.region_id for j in tmp_regions], 'id does not exist'
                edited_city.region_id = chosen_region
            edited_city.city_name = new_name
            session.commit()
            print('Edit succeeded')
        except ValueError:
            print('input incorrect')
        except AssertionError:
            print('chosen id does not exist')

    @staticmethod
    def delete_region():
        tmp_regions = session.query(Region).all()
        for i in tmp_regions:
            print("{}. {}".format(i.region_id, i.region_name))
        try:
            chosen_region = int(input('Choose a region to add a city (type number of chosen region) '))
            assert chosen_region in [j.region_id for j in tmp_regions], 'id does not exist'
            query1 = session.query(City).filter(City.region_id == chosen_region).delete()
            query2 = session.query(Region).filter(Region.region_id == chosen_region).delete()
            session.commit()
            print('Delete succeeded')
        except AssertionError:
            print('chosen number does not exist')
        except ValueError:
            print('input incorrect')

    @staticmethod
    def delete_city():
        tmp_cities = session.query(City).all()
        for i in tmp_cities:
            print('{}. {}'.format(i.city_id, i.city_name))
        try:
            chosen_city = int(input('Type number of chosen city '))
            assert chosen_city in [j.city_id for j in tmp_cities], 'id does not exist'
            query = session.query(City).filter(City.city_id == chosen_city).delete()
            session.commit()
            print('Delete succeeded')
        except ValueError:
            print('input incorrect')
        except AssertionError:
            print('chosen id does not exist')


# main body
Base.metadata.create_all(engine)  # creating tables from schema(no affect if tables already exist)
my_help = 'Laboratory work #6\n'\
        'Made by Oleksandr Korienev, student of iv-72\n'\
        'Only English is supported, cyrillic symbols can cause a crash\n'\
        'available commands:\n'\
        '\'add_region\' to add new region to the database\n'\
        '\'add_city\' to add new city to the database\n'\
        '\'edit_region\' to edit region \n'\
        '\'edit_city\' to edit city\n'\
        '\'delete_region\' to delete region from database (deleting region will cause deleting'\
        'all cities which are linked to it!)\n'\
        '\'delete_city\' to delete city from the database\n'\
        '\'continue\' to finish the work with database'

while True:
    main_choice = input('choose an option, \'help\' to display help ')
    if main_choice == 'add_region':
        DBCONTROLLERS.add_region()
    elif main_choice == 'help':
        print(my_help)
    elif main_choice == 'add_city':
        DBCONTROLLERS.add_city()
    elif main_choice == 'edit_region':
        DBCONTROLLERS.edit_region()
    elif main_choice == 'edit_city':
        DBCONTROLLERS.edit_city()
    elif main_choice == 'delete_region':
        DBCONTROLLERS.delete_region()
    elif main_choice == 'delete_city':
        DBCONTROLLERS.delete_city()
    elif main_choice == 'continue':
        break
    else:
        print('unknown command')

region_objects_list = []
regions = session.query(Region).all()
raw_region_list = [[i.region_id, i.region_name, i.region_population, i.region_square] for i in regions]
for i in raw_region_list:
    city_query = session.query(City).filter(City.region_id == i[0]).all()
    tmp_cities = [j.city_name for j in city_query]
    i.append(tmp_cities)
    region_objects_list.append(REGION(i[1:]))
for i in region_objects_list:
    print(i)
