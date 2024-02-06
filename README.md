# Influence_Difussion
### In elasticsearch stores 2 index, called "sent_text_test01" and "received_text_test01"


## 1. Download Database
### 1.1 ElasticSearch 7.7  - Elasticsearch: https://www.elastic.co/downloads/past-releases/elasticsearch-7-7-0
### 1.2 Kibana 7.7 - Kibana: https://www.elastic.co/downloads/past-releases/kibana-7-7-0

## 2. Setup the index mapping in elasticsearch
### 2.1. user_sent_messages
Run following script in kibana (http://localhost:5601)

```JSON
PUT /sent_text_test01

{
  "mapping": {
    "_doc": {
      "properties": {
        "from": {
          "type": "text"
        },
        "node": {
          "type": "text"
        },
        "sent_text": {
          "type": "text"
        },
        "sent_text_vector": {
          "type": "dense_vector",
          "dims": 384
        },
        "to": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      }
    }
  }
}
```

### 2.2. user_received_messages
Run following script in kibana (http://localhost:5601)

```JSON
PUT received_text_test01

{
  "mapping": {
    "_doc": {
      "properties": {
        "from": {
          "type": "text"
        },
        "last_id": {
          "type": "long"
        },
        "node": {
          "type": "text"
        },
        "received_text": {
          "type": "text"
        },
        "received_text_vector": {
          "type": "dense_vector",
          "dims": 384
        },
        "received_text_weight": {
          "type": "float"
        },
        "sent_text": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "sent_text_vector": {
          "type": "float"
        }
      }
    }
  }
}
```

## 3. Download reuqirements.txt
RUN: 
pip install -r requirements.txt