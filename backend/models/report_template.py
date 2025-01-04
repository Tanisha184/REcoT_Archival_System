from pymongo import MongoClient

class ReportTemplate:
    def __init__(self, name, template_type, fields, layout):
        self.name = name
        self.template_type = template_type  # e.g., 'department_summary', 'task_detail'
        self.fields = fields  # List of fields to include in report
        self.layout = layout  # Template layout configuration

class ReportTemplateModel:
    def __init__(self, db):
        self.db = db
        self.collection = self.db['report_templates']

    def create_template(self, name, template_type, fields, layout):
        template = {
            'name': name,
            'template_type': template_type,
            'fields': fields,
            'layout': layout,
            'created_at': datetime.now()
        }
        return self.collection.insert_one(template)

    def get_all_templates(self):
        return list(self.collection.find({}))

    def get_template_by_name(self, name):
        return self.collection.find_one({'name': name})

    def update_template(self, name, updates):
        return self.collection.update_one(
            {'name': name},
            {'$set': updates}
        )

    def delete_template(self, name):
        return self.collection.delete_one({'name': name})
