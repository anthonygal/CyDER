import docker_django.apps.cyder.models as m
import csv

def database_initialization(filename='/usr/src/app/docker_django/static/init_DB.csv'):
    """
    Initialize the database from a csv file.
    (remove previous instances)
    """
    # Counter
    model_added = 0

    # Remove existing model from the database
    all_model = m.Model.objects.all()
    for instance in all_model:
        instance.delete()

    # Read csv file
    with open(filename, 'rb') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        # Each row define a distribution grid model
        for row in spamreader:
            new_entry = {
                'filename': row['filename'],
                'lat': row['lat'],
                'lon': row['lon'],
                'breaker_name': row['breaker_name'],
                'city': row['city'],
                'area': row['area'],
                'region': row['region'],
                'zip_code': row['zip_code'],
                'version': row['version'],
                'upmu_location': row['upmu_location'],
            }

            new_model = m.Model(**new_entry)
            new_model.save()
            model_added += 1

    print("You have added " + str(model_added) + " distribution models")
    return True