import json
import sys

def clean_records(input_path, output_path):
    # 1. Open and load the raw GeoJSON file
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    cleaned_features = []

    # 2. Loop through features and apply your cleaning logic
    for feature in data.get('features', []):
        geometry = feature.get('geometry')
        properties = feature.get('properties', {})
        
        # Clean up or standardize taxon names
        taxon_name = properties.get('s', '')
        
        # Example fixes or regex cleanups:
        if taxon_name == "Lizonia (Cesati":
            properties['s'] = "Lizonia"  # Or your desired corrected string
        elif taxon_name.endswith("("):
            properties['s'] = taxon_name.rstrip("(").strip()
            
        # Make sure properties are saved back to the feature
        feature['properties'] = properties
        
        # Ensure the feature has valid geometry coordinates before keeping it
        if geometry and geometry.get('coordinates'):
            cleaned_features.append(feature)
            
    # 3. Update the GeoJSON structure with the cleaned features
    data['features'] = cleaned_features
    
    # 4. Write out the cleaned records to the target path
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        
    print(f"Successfully cleaned {len(cleaned_features)} records and saved to {output_path}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python clean_records.py <input_geojson> <output_geojson>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    clean_records(input_file, output_file)
