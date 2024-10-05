# models.py

from bson import ObjectId


class MongoOperations:
    def __init__(self, mongo):
        self.mongo = mongo
        pass
    
    def serialize_sales_record(self,sales_record):
     sales_record["_id"] = str(sales_record["_id"])  # Convert ObjectId to string
     return sales_record
    
    def create_sales_record(self, user_id, data):
        sales_record = {
            "user": user_id,
            "product_name": data["product_name"],
            "amount": data["amount"],
            "date_of_sale": data["date_of_sale"],
            "status": data["status"],
        }
        result = self.mongo.db.sales.insert_one(sales_record)
        sales_record["_id"] = str(result.inserted_id)  # Convert ObjectId to string after insertion
        return self.serialize_sales_record(sales_record)

    def get_sales_records(self, user_id):
        sales_records = self.mongo.db.sales.find({"user": user_id})
        return [self.serialize_sales_record(record) for record in sales_records]

    def get_sales_record_by_id(self, sale_id, user_id):
        # Get a specific sales record by its ID for the user
        record = self.mongo.db.sales.find_one({'_id': ObjectId(sale_id), 'user': user_id})
        if record:
            return self.serialize_sales_record(record)
        return {"message": "Record not found"}, 404

    def update_sales_record(self, sale_id, data, user_id):
        # Update a sales record
        result = self.mongo.db.sales.update_one(
            {'_id': ObjectId(sale_id), 'user': user_id},
            {"$set": data}
        )
        if result.modified_count > 0:
            return {"message": "Record updated"}
        return {"message": "Record not found or no changes made"}, 404

    def delete_sales_record(self, sale_id, user_id):
        # Delete a sales record
        result = self.mongo.db.sales.delete_one({"_id": ObjectId(sale_id), "user": user_id})
        if result.deleted_count > 0:
            return {"message": "Record deleted"}
        return {"message": "Record not found"}, 404
