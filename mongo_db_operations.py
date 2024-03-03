import datetime
import pprint
import pymongo

# Função para criar uma conexão com o MongoDB
def connect_to_mongodb(username, password, cluster_url, database_name='test'):
    try:
        client = pymongo.MongoClient(
            f"mongodb+srv://{username}:{password}@{cluster_url}/{database_name}?retryWrites=true&w=majority"
        )
        db = client[database_name]
        return client, db.posts
    except pymongo.errors.ConfigurationError as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        exit()

# Função para inserir um único post
def insert_single_post(posts_collection):
    post = {
        "author": "Valdemar",
        "text": "My first MongoDB application based on Python",
        "tags": ["mongodb", "python3", "pymongo"],
        "date": datetime.datetime.utcnow()
    }

    post_id = posts_collection.insert_one(post).inserted_id
    print(f"ID do post inserido: {post_id}")

# Função para inserir múltiplos posts
def insert_multiple_posts(posts_collection):
    new_posts = [
        {
            "author": "Valdemar",
            "text": "Another post",
            "tags": ["bulk", "post", "insert"],
            "date": datetime.datetime.utcnow()
        },
        {
            "author": "Joao",
            "text": "Post from Joao. New post available",
            "title": "Mongo is fun",
            "date": datetime.datetime(2011, 18, 46, 6, 45)
        }
    ]

    result = posts_collection.insert_many(new_posts)
    print(f"\nIDs dos posts inseridos em massa: {result.inserted_ids}")

# Função para recuperar documentos por autor
def retrieve_by_author(posts_collection, author):
    print(f"\nRecuperação por autor ({author}):")
    pprint.pprint(posts_collection.find_one({"author": author}))

# Função para exibir todos os documentos na coleção
def display_all_documents(posts_collection):
    print("\nDocumentos presentes na coleção posts:")
    for post in posts_collection.find():
        pprint.pprint(post)

def main():
    # Substitua <USERNAME>, <PASSWORD> e <CLUSTER_URL> com suas credenciais reais
    client, posts = connect_to_mongodb("<USERNAME>", "<PASSWORD>", "<cluster_url>")
    
    with client:
        insert_single_post(posts)
        insert_multiple_posts(posts)
        retrieve_by_author(posts, "Joao")
        display_all_documents(posts)

if __name__ == "__main__":
    main()
