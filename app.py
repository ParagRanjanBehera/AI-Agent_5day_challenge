import os
import re
import requests
import xml.etree.ElementTree as ET
from flask import Flask, jsonify, render_template, request
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

# Simple in-memory cache
cache = {
    "data": None,
    "last_fetched": None
}

FEED_URL = "https://docs.cloud.google.com/feeds/bigquery-release-notes.xml"

def parse_release_notes(xml_content):
    """
    Parses the Atom XML feed of BigQuery release notes and extracts structured data.
    """
    # Atom feeds use the namespace: http://www.w3.org/2005/Atom
    # Some XML parsers require namespace mapping
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        # Try stripping namespaces or encoding if standard parsing fails
        # or clean up common XML bugs
        print(f"XML Parsing Error: {e}")
        raise e

    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    entries = []
    
    for idx, entry_elem in enumerate(root.findall('atom:entry', ns)):
        title_elem = entry_elem.find('atom:title', ns)
        updated_elem = entry_elem.find('atom:updated', ns)
        id_elem = entry_elem.find('atom:id', ns)
        link_elem = entry_elem.find('atom:link[@rel="alternate"]', ns)
        content_elem = entry_elem.find('atom:content', ns)
        
        date_str = title_elem.text if title_elem is not None else "Unknown Date"
        updated_str = updated_elem.text if updated_elem is not None else ""
        entry_id = id_elem.text if id_elem is not None else f"note-{idx}"
        link_url = link_elem.attrib.get('href', '') if link_elem is not None else ''
        content_html = content_elem.text if content_elem is not None else ''
        
        # Parse the HTML content to break down updates by their h3 category (Feature, Announcement, etc.)
        soup = BeautifulSoup(content_html, 'html.parser')
        updates = []
        
        current_type = None
        current_content = []
        
        for child in soup.children:
            if child.name == 'h3':
                if current_type is not None or current_content:
                    updates.append({
                        "type": current_type or "Update",
                        "description_html": "".join(str(x) for x in current_content).strip()
                    })
                    current_content = []
                current_type = child.get_text(strip=True)
            elif child.name is not None:
                current_content.append(child)
            elif str(child).strip():
                current_content.append(child)
                
        if current_type is not None or current_content:
            updates.append({
                "type": current_type or "Update",
                "description_html": "".join(str(x) for x in current_content).strip()
            })
            
        # Try to parse date string for sorting/formatting
        parsed_date = None
        # Format June 17, 2026
        try:
            parsed_date = datetime.strptime(date_str.strip(), "%B %d, %Y").strftime("%Y-%m-%d")
        except ValueError:
            # Fallback to updated tag timestamp
            if updated_str:
                try:
                    parsed_date = updated_str[:10] # YYYY-MM-DD
                except Exception:
                    pass
            if not parsed_date:
                parsed_date = "1970-01-01"

        entries.append({
            "id": entry_id,
            "date": date_str,
            "sort_date": parsed_date,
            "updated": updated_str,
            "link": link_url,
            "updates": updates
        })
        
    # Sort entries by date descending
    entries.sort(key=lambda x: x['sort_date'], reverse=True)
    return entries

def fetch_feed(force_refresh=False):
    """
    Fetches the feed from the remote URL, caching the parsed result.
    """
    global cache
    
    if not force_refresh and cache["data"] is not None:
        return cache["data"], "cache"
        
    try:
        # Google docs feeds sometimes require a standard user agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(FEED_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # Parse XML
        parsed_entries = parse_release_notes(response.content)
        
        # Update cache
        cache["data"] = parsed_entries
        cache["last_fetched"] = datetime.now().isoformat()
        
        return parsed_entries, "fresh"
    except Exception as e:
        print(f"Error fetching feed: {e}")
        # If remote fetch fails, return cached data if available
        if cache["data"] is not None:
            return cache["data"], "fallback_cache"
        raise e

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes')
def get_notes():
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    try:
        data, status = fetch_feed(force_refresh=force_refresh)
        return jsonify({
            "success": True,
            "status": status,
            "last_fetched": cache["last_fetched"],
            "count": len(data),
            "notes": data
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    # Default Flask port
    app.run(host='0.0.0.0', port=5000, debug=True)
