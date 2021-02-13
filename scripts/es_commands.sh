# List of usefule ES commands.

# Check indices and their status.
curl "localhost:9200/_cat/indices?v=true"

# Update index to read-only.
curl -X PUT "localhost:9200/sample_blocks/_settings?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index.blocks.write": true
  }
}
'

# Update number of shards for index.
curl -X POST "localhost:9200/sample_blocks/_split/split-sample_blocks?pretty" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "index.number_of_shards": 3
  }
}
'

