from langchain_elasticsearch import ElasticsearchStore
from langchain_community.embeddings import OllamaEmbeddings

def load_fake_data():
    embeddings = OllamaEmbeddings(model="qwen3-embedding:0.6b", base_url="http://host.docker.internal:11434")

    fake_products = [
        {
            "name": "Apple iPhone 15 Pro Max 256 GB",
            "category": "Elektronik",
            "price": "74.999 TL",
            "description": "Apple'ın en yeni ve en güçlü akıllı telefonu. Titan kasası, A17 Pro çipi ve gelişmiş kamera sistemi ile öne çıkıyor."
        },
        {
            "name": "Samsung Galaxy S24 Ultra 512 GB",
            "category": "Elektronik",
            "price": "69.999 TL",
            "description": "Samsung'un en üst düzey akıllı telefonu. Dahili S Pen, yapay zeka özellikleri ve güçlü kamerası ile dikkat çekiyor."
        },
        {
            "name": "Sony Playstation 5 Slim",
            "category": "Oyun Konsolu",
            "price": "24.999 TL",
            "description": "Sony'nin popüler oyun konsolunun daha ince ve hafif versiyonu. 4K oyun deneyimi ve hızlı SSD'si ile oyunseverlerin tercihi."
        },
        {
            "name": "Microsoft Xbox Series X",
            "category": "Oyun Konsolu",
            "price": "22.999 TL",
            "description": "Microsoft'un en güçlü oyun konsolu. 4K oyun, hızlı yükleme süreleri ve geniş oyun kütüphanesi ile öne çıkıyor."
        },
        {
            "name": "Apple MacBook Pro 16 inch M3 Max",
            "category": "Bilgisayar",
            "price": "99.999 TL",
            "description": "Profesyoneller için tasarlanmış güçlü bir dizüstü bilgisayar. M3 Max çipi, Liquid Retina XDR ekranı ve uzun pil ömrü ile fark yaratıyor."
        },
        {
            "name": "Dell XPS 15 Laptop",
            "category": "Bilgisayar",
            "price": "59.999 TL",
            "description": "Şık tasarımı ve yüksek performansı bir araya getiren bir dizüstü bilgisayar. InfinityEdge ekranı ve güçlü donanımı ile öne çıkıyor."
        },
        {
            "name": "LG OLED C3 65 inch TV",
            "category": "Televizyon",
            "price": "49.999 TL",
            "description": "LG'nin en yeni OLED televizyonu. Mükemmel siyahlar, canlı renkler ve akıllı TV özellikleri ile sinema keyfini evinize getiriyor."
        },
        {
            "name": "Samsung QN90C 75 inch TV",
            "category": "Televizyon",
            "price": "64.999 TL",
            "description": "Samsung'un Neo QLED teknolojisine sahip televizyonu. Yüksek parlaklık, Quantum Dot renkleri ve gelişmiş ses sistemi ile etkileyici bir izleme deneyimi sunuyor."
        },
        {
            "name": "Bose QuietComfort Ultra Headphones",
            "category": "Kulaklık",
            "price": "12.999 TL",
            "description": "Bose'un en yeni gürültü engelleyici kulaklığı. Üstün ses kalitesi, konforlu tasarımı ve etkili gürültü engelleme özelliği ile öne çıkıyor."
        },
        {
            "name": "Sony WH-1000XM5 Headphones",
            "category": "Kulaklık",
            "price": "10.999 TL",
            "description": "Sony'nin popüler gürültü engelleyici kulaklığının en yeni modeli. Geliştirilmiş gürültü engelleme, yüksek çözünürlüklü ses ve uzun pil ömrü sunuyor."
        },
    ]

    texts = [f"Ürün Adı: {p['name']}\nKategori: {p['category']}\nFiyat: {p['price']}\nAçıklama: {p['description']}" for p in fake_products]

    vector_store = ElasticsearchStore(
        es_url="http://elasticsearch:9200",
        index_name="products",
        embedding=embeddings
    )

    vector_store.add_texts(texts)

if __name__ == "__main__":
    load_fake_data()