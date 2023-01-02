import logging

from src.domain.article import Article
from boto3.dynamodb.conditions import Key

logger = logging.getLogger()


class ArticleDao:
    def __init__(self, dynamodb_resource, dynamodb_client, table_name):
        self.dynamodb_resource = dynamodb_resource
        self.dynamodb_client = dynamodb_client
        self.table = self.dynamodb_resource.Table(table_name)

    def create(self, entity: Article) -> None:
        logger.info("[entity] create")
        self.table.put_item(Item=entity.to_dict())

    def delete(self, uuid) -> None:
        logger.info("[entity] delete")

        result = self.table.query(
            IndexName="uuid",
            KeyConditionExpression=Key("uuid").eq(uuid),
        )

        author = result["Items"][0]["author"]
        title = result["Items"][0]["title"]
        self.table.delete_item(Key={"author": author, "title": title})

        return None

    def get_by_uuid(self, uuid) -> Article:
        logger.info("[entity] entity")

        result = self.table.query(
            IndexName="uuid",
            KeyConditionExpression=Key("uuid").eq(uuid),
        )

        if "Items" not in result:
            return None

        return result["Items"][0] if len(result["Items"]) == 1 else None

    def find_by_tag(self, tag):
        logging.info("[article] find_by_tag")

        result = self.table.query(
            IndexName="tags",
            KeyConditionExpression=Key("tags").eq(tag),
        )

        print(result)

        return result["Items"] if "Items" in result else None
