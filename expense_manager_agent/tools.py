# expense_manager_agent/tools.py

import datetime
from typing import Dict, List, Any
from google.cloud import firestore
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1 import FieldFilter
from google.cloud.firestore_v1.base_query import And
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from settings import get_settings
from google import genai
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SETTINGS = get_settings()
DB_CLIENT = firestore.Client(
    project=SETTINGS.GCLOUD_PROJECT_ID
    # database=SETTINGS.FIRESTORE_DATABASE_ID
)  
COLLECTION = DB_CLIENT.collection(SETTINGS.DB_COLLECTION_NAME)
GENAI_CLIENT = genai.Client(
    vertexai=True, location=SETTINGS.GCLOUD_LOCATION, project=SETTINGS.GCLOUD_PROJECT_ID
)
EMBEDDING_DIMENSION = 768
EMBEDDING_FIELD_NAME = "embedding"
INVALID_ITEMS_FORMAT_ERR = """
Invalid items format. Must be a list of dictionaries with 'name', 'price', and 'quantity' keys."""
RECEIPT_DESC_FORMAT = """
Store Name: {store_name}
Transaction Time: {transaction_time}
Total Amount: {total_amount}
Currency: {currency}
Purchased Items:
{purchased_items}
Receipt Image ID: {receipt_id}
"""

# Predefined categories for expenses
ITEM_CATEGORIES = [
    "Groceries", "Dining", "Entertainment", "Fitness", 
    "Electronics", "Clothing", "Healthcare", "Transportation",
    "Utilities", "Education", "Home", "Personal Care", 
    "Travel", "Gifts", "Business", "Other"
]

# Common items and their categories for fallback categorization
COMMON_ITEMS = {
    # Groceries
    "milk": "Groceries", "bread": "Groceries", "eggs": "Groceries", 
    "rice": "Groceries", "cereal": "Groceries", "pasta": "Groceries",
    "vegetables": "Groceries", "fruits": "Groceries", "meat": "Groceries",
    "chicken": "Groceries", "beef": "Groceries", "fish": "Groceries",
    "cheese": "Groceries", "yogurt": "Groceries", "butter": "Groceries",
    "spoon": "Groceries", "fork": "Groceries", "plate": "Groceries",
    
    # Dining
    "restaurant": "Dining", "cafe": "Dining", "coffee": "Dining",
    "lunch": "Dining", "dinner": "Dining", "breakfast": "Dining",
    "burger": "Dining", "pizza": "Dining", "sandwich": "Dining",
    "takeout": "Dining", "delivery": "Dining", "food delivery": "Dining",
    
    # Entertainment
    "movie": "Entertainment", "ticket": "Entertainment", "cinema": "Entertainment",
    "concert": "Entertainment", "show": "Entertainment", "game": "Entertainment",
    "netflix": "Entertainment", "spotify": "Entertainment", "subscription": "Entertainment",
    
    # Electronics
    "phone": "Electronics", "laptop": "Electronics", "computer": "Electronics",
    "tv": "Electronics", "headphones": "Electronics", "charger": "Electronics",
    "camera": "Electronics", "tablet": "Electronics", "speaker": "Electronics",
    "light": "Electronics", "bulb": "Electronics", "battery": "Electronics",
    
    # Clothing
    "shirt": "Clothing", "pants": "Clothing", "dress": "Clothing",
    "shoes": "Clothing", "jacket": "Clothing", "hat": "Clothing",
    "socks": "Clothing", "underwear": "Clothing", "sweater": "Clothing",
    "apparel": "Clothing", "cloth": "Clothing", "fashion": "Clothing",
    
    # Transportation
    "gas": "Transportation", "fuel": "Transportation", "uber": "Transportation",
    "taxi": "Transportation", "bus": "Transportation", "train": "Transportation",
    "subway": "Transportation", "car rental": "Transportation", "parking": "Transportation",
    
    # Healthcare
    "medicine": "Healthcare", "doctor": "Healthcare", "pharmacy": "Healthcare",
    "hospital": "Healthcare", "dental": "Healthcare", "prescription": "Healthcare",
    "vitamin": "Healthcare", "supplement": "Healthcare", "insurance": "Healthcare",
    
    # Personal Care
    "soap": "Personal Care", "shampoo": "Personal Care", "toothpaste": "Personal Care",
    "lotion": "Personal Care", "haircut": "Personal Care", "makeup": "Personal Care",
    "razor": "Personal Care", "deodorant": "Personal Care", "cosmetics": "Personal Care",
    "sponge": "Personal Care", "scrub": "Personal Care", "brush": "Personal Care",
    
    # Home
    "doormat": "Home", "mat": "Home", "knife": "Home", "kitchen": "Home",
    "jar": "Home", "container": "Home", "grater": "Home", "utensil": "Home",
    "clip": "Home", "duster": "Home", "broom": "Home", "mop": "Home",
    "wipe": "Home", "cleaner": "Home", "towel": "Home", "bedsheet": "Home",
    "pillow": "Home", "curtain": "Home", "cloth": "Home", "wire": "Home",
    "thali": "Home", "plate": "Home", "glass": "Home", "cup": "Home",
    "bowl": "Home", "pan": "Home", "pot": "Home", "tope": "Home",
    "chalni": "Home", "strainer": "Home", "basket": "Home", "hanger": "Home",
    "wati": "Home", "bag": "Home", "shopping": "Home", "hati": "Home"
}

# Define a more detailed format for displaying items with categories
ITEM_DISPLAY_FORMAT = "{name} (${price:.2f}) - Category: {category} - Quantity: {quantity} - Tax: ${tax:.2f}"


def format_purchased_items(items):
    """
    Format purchased items for display, including their categories.
    
    Args:
        items (List[Dict]): List of purchased items
        
    Returns:
        str: Formatted string with item details including categories
    """
    if not items:
        return "No items"
        
    formatted_items = []
    for item in items:
        try:
            category = item.get("category", "Uncategorized")
            name = item.get("name", "Unknown item")
            price = item.get("price", 0.0)
            quantity = item.get("quantity", 1)
            tax = item.get("tax", 0.0)
            
            formatted_item = f"{name} (${price:.2f}) - Category: {category} - Quantity: {quantity} - Tax: ${tax:.2f}"
            formatted_items.append(formatted_item)
        except Exception as e:
            formatted_items.append(f"Error formatting item: {str(e)}")
    
    return "\n".join(formatted_items)


def categorize_item(item_name: str) -> str:
    """
    Categorize an item based on its name using AI model.
    
    Args:
        item_name (str): The name of the item to categorize.
        
    Returns:
        str: The category of the item.
    """
    try:
        logger.info(f"Categorizing item: {item_name}")
        
        # We'll rely primarily on the AI model for categorization
        logger.info(f"Using Gemini model for categorization")
        
        # Create prompt for the model with more detailed context about categories
        prompt = f"""
        You are an expense categorization expert. Your task is to categorize this item into the most appropriate expense category.

        Here are the available categories with examples of what might be included in each:
        - Groceries: Food items, kitchen utensils, cooking supplies, spoons, plates, grocery store purchases
        - Dining: Restaurant meals, cafes, food delivery
        - Entertainment: Movies, shows, subscriptions, games
        - Fitness: Gym equipment, fitness classes, sports gear
        - Electronics: Gadgets, appliances, lights, electronics, tech items
        - Clothing: Clothes, fashion items, accessories, apparel
        - Healthcare: Medicine, medical services, health supplements
        - Transportation: Travel costs, gas, fuel, vehicles, transportation items
        - Utilities: Electricity, water, internet bills
        - Education: Books, courses, school supplies
        - Home: Household items, kitchenware, home decor, furniture, mats, containers, cleaning supplies
        - Personal Care: Toiletries, hygiene products, cosmetics, personal grooming items
        - Travel: Vacation expenses, hotels, flights
        - Gifts: Presents, gift items
        - Business: Office supplies, business expenses
        - Other: Miscellaneous items that don't fit other categories

        Item to categorize: {item_name}

        Based on the item name, choose the MOST appropriate category from the list above.
        Household items like kitchen utensils, containers, cleaning supplies, home decor should be categorized as "Home".
        
        Return ONLY the category name, nothing else.
        """
        
        # Get response from Gemini with temperature set to 0 for more consistent responses
        response = GENAI_CLIENT.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt,
            generation_config={"temperature": 0.0}
        )
        
        category = response.text.strip()
        logger.info(f"Raw category from model: {category}")
        
        # Verify the category is in our list (case-insensitive)
        category_upper = category.upper()
        for valid_category in ITEM_CATEGORIES:
            if valid_category.upper() == category_upper:
                logger.info(f"Matched category: {valid_category}")
                return valid_category
        
        # Try fuzzy matching by checking if any category appears within the response
        for valid_category in ITEM_CATEGORIES:
            if valid_category.upper() in category_upper:
                logger.info(f"Fuzzy matched category: {valid_category}")
                return valid_category
                
        # If not in our list, default to "Other"
        logger.info(f"No matching category found, defaulting to 'Other'")
        return "Other"
    except Exception as e:
        logger.error(f"Error categorizing item: {str(e)}")
        return "Other"  # Default fallback


def sanitize_image_id(image_id: str) -> str:
    """Sanitize image ID by removing any leading/trailing whitespace."""
    if image_id.startswith("[IMAGE-"):
        image_id = image_id.split("ID ")[1].split("]")[0]

    return image_id.strip()


def store_receipt_data(
    image_id: str,
    store_name: str,
    transaction_time: str,
    total_amount: float,
    purchased_items: List[Dict[str, Any]],
    currency: str = "IDR",
) -> str:
    """
    Store receipt data in the database.

    Args:
        image_id (str): The unique identifier of the image. For example IMAGE-POSITION 0-ID 12345,
            the ID of the image is 12345.
        store_name (str): The name of the store.
        transaction_time (str): The time of purchase, in ISO format ("YYYY-MM-DDTHH:MM:SS.ssssssZ").
        total_amount (float): The total amount spent.
        purchased_items (List[Dict[str, Any]]): A list of items purchased with their prices. Each item must have:
            - name (str): The name of the item.
            - price (float): The price of the item.
            - quantity (int, optional): The quantity of the item. Defaults to 1 if not provided.
        currency (str, optional): The currency of the transaction, can be derived from the store location.
            If unsure, default is "IDR".

    Returns:
        str: A success message with the receipt ID.

    Raises:
        Exception: If the operation failed or input is invalid.
    """
    try:
        # In case of it provide full image placeholder, extract the id string
        image_id = sanitize_image_id(image_id)

        # Check if the receipt already exists
        doc = get_receipt_data_by_image_id(image_id)

        if doc:
            return f"Receipt with ID {image_id} already exists"

        # Validate transaction time
        if not isinstance(transaction_time, str):
            raise ValueError(
                "Invalid transaction time: must be a string in ISO format 'YYYY-MM-DDTHH:MM:SS.ssssssZ'"
            )
        try:
            datetime.datetime.fromisoformat(transaction_time.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError(
                "Invalid transaction time format. Must be in ISO format 'YYYY-MM-DDTHH:MM:SS.ssssssZ'"
            )

        # Validate items format
        if not isinstance(purchased_items, list):
            raise ValueError(INVALID_ITEMS_FORMAT_ERR)

        # Create a new list for items with categories
        categorized_items = []
        
        for _item in purchased_items:
            if (
                not isinstance(_item, dict)
                or "name" not in _item
                or "price" not in _item
            ):
                raise ValueError(INVALID_ITEMS_FORMAT_ERR)

            # Create a new item dict with all original fields
            new_item = dict(_item)
            
            # Ensure quantity is set
            if "quantity" not in new_item:
                new_item["quantity"] = 1
                
            # Add tax information if not provided
            if "tax" not in new_item:
                # Default tax to 0 if not specified
                new_item["tax"] = 0.0
                logger.info(f"Added default tax (0.0) to item '{new_item['name']}'")
                
            # Add category if not provided
            if "category" not in new_item or not new_item["category"]:
                category = categorize_item(new_item["name"])
                new_item["category"] = category
                logger.info(f"Added category '{category}' to item '{new_item['name']}'")
                
            # Add the categorized item to our new list
            categorized_items.append(new_item)
            
        logger.info(f"Processed {len(categorized_items)} items with categories")
        for idx, item in enumerate(categorized_items):
            logger.info(f"Item {idx+1}: {item['name']} - Category: {item.get('category', 'None')}")
            
        # Debug log the final structure that will be stored in Firestore
        logger.info(f"Final categorized items structure: {categorized_items}")

        # Create a combined text from all receipt information for better embedding
        formatted_items = format_purchased_items(categorized_items)
        
        result = GENAI_CLIENT.models.embed_content(
            model="text-embedding-004",
            contents=RECEIPT_DESC_FORMAT.format(
                store_name=store_name,
                transaction_time=transaction_time,
                total_amount=total_amount,
                currency=currency,
                purchased_items=formatted_items,  # Use the formatted items
                receipt_id=image_id,
            ),
        )

        embedding = result.embeddings[0].values

        doc = {
            "receipt_id": image_id,
            "store_name": store_name,
            "transaction_time": transaction_time,
            "total_amount": total_amount,
            "currency": currency,
            "purchased_items": categorized_items,  # Use the new categorized items list
            EMBEDDING_FIELD_NAME: Vector(embedding),
        }

        COLLECTION.add(doc)

        return f"Receipt stored successfully with ID: {image_id}"
    except Exception as e:
        raise Exception(f"Failed to store receipt: {str(e)}")


def search_receipts_by_metadata_filter(
    start_time: str,
    end_time: str,
    min_total_amount: float = -1.0,
    max_total_amount: float = -1.0,
) -> str:
    """
    Filter receipts by metadata within a specific time range and optionally by amount.

    Args:
        start_time (str): The start datetime for the filter (in ISO format, e.g. 'YYYY-MM-DDTHH:MM:SS.ssssssZ').
        end_time (str): The end datetime for the filter (in ISO format, e.g. 'YYYY-MM-DDTHH:MM:SS.ssssssZ').
        min_total_amount (float): The minimum total amount for the filter (inclusive). Defaults to -1.
        max_total_amount (float): The maximum total amount for the filter (inclusive). Defaults to -1.

    Returns:
        str: A string containing the list of receipt data matching all applied filters.

    Raises:
        Exception: If the search failed or input is invalid.
    """
    try:
        # Validate start and end times
        if not isinstance(start_time, str) or not isinstance(end_time, str):
            raise ValueError("start_time and end_time must be strings in ISO format")
        try:
            datetime.datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            datetime.datetime.fromisoformat(end_time.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("start_time and end_time must be strings in ISO format")

        # Start with the base collection reference
        query = COLLECTION

        # Build the composite query by properly chaining conditions
        # Notes that this demo assume 1 user only,
        # need to refactor the query for multiple user
        filters = [
            FieldFilter("transaction_time", ">=", start_time),
            FieldFilter("transaction_time", "<=", end_time),
        ]

        # Add optional filters
        if min_total_amount != -1:
            filters.append(FieldFilter("total_amount", ">=", min_total_amount))

        if max_total_amount != -1:
            filters.append(FieldFilter("total_amount", "<=", max_total_amount))

        # Apply the filters
        composite_filter = And(filters=filters)
        query = query.where(filter=composite_filter)

        # Execute the query and collect results
        search_result_description = "Search by Metadata Results:\n"
        for doc in query.stream():
            data = doc.to_dict()
            data.pop(
                EMBEDDING_FIELD_NAME, None
            )  # Remove embedding as it's not needed for display
            
            # Format the purchased items with categories
            if "purchased_items" in data:
                formatted_items = format_purchased_items(data["purchased_items"])
                data_copy = dict(data)
                data_copy["purchased_items"] = formatted_items
                search_result_description += f"\n{RECEIPT_DESC_FORMAT.format(**data_copy)}"
            else:
                search_result_description += f"\n{RECEIPT_DESC_FORMAT.format(**data)}"

        return search_result_description
    except Exception as e:
        raise Exception(f"Error filtering receipts: {str(e)}")


def search_relevant_receipts_by_natural_language_query(
    query_text: str, limit: int = 5
) -> str:
    """
    Search for receipts with content most similar to the query using vector search.
    This tool can be use for user query that is difficult to translate into metadata filters.
    Such as store name or item name which sensitive to string matching.
    Use this tool if you cannot utilize the search by metadata filter tool.

    Args:
        query_text (str): The search text (e.g., "coffee", "dinner", "groceries").
        limit (int, optional): Maximum number of results to return (default: 5).

    Returns:
        str: A string containing the list of contextually relevant receipt data.

    Raises:
        Exception: If the search failed or input is invalid.
    """
    try:
        # Generate embedding for the query text
        result = GENAI_CLIENT.models.embed_content(
            model="text-embedding-004", contents=query_text
        )
        query_embedding = result.embeddings[0].values

        # Notes that this demo assume 1 user only,
        # need to refactor the query for multiple user
        vector_query = COLLECTION.find_nearest(
            vector_field=EMBEDDING_FIELD_NAME,
            query_vector=Vector(query_embedding),
            distance_measure=DistanceMeasure.EUCLIDEAN,
            limit=limit,
        )

        # Execute the query and collect results
        search_result_description = "Search by Contextual Relevance Results:\n"
        for doc in vector_query.stream():
            data = doc.to_dict()
            data.pop(
                EMBEDDING_FIELD_NAME, None
            )  # Remove embedding as it's not needed for display
            
            # Format the purchased items with categories
            if "purchased_items" in data:
                formatted_items = format_purchased_items(data["purchased_items"])
                data_copy = dict(data)
                data_copy["purchased_items"] = formatted_items
                search_result_description += f"\n{RECEIPT_DESC_FORMAT.format(**data_copy)}"
            else:
                search_result_description += f"\n{RECEIPT_DESC_FORMAT.format(**data)}"

        return search_result_description
    except Exception as e:
        raise Exception(f"Error searching receipts: {str(e)}")


def get_receipt_data_by_image_id(image_id: str) -> Dict[str, Any]:
    """
    Retrieve receipt data from the database using the image_id.

    Args:
        image_id (str): The unique identifier of the receipt image. For example, if the placeholder is
            [IMAGE-ID 12345], the ID to use is 12345.

    Returns:
        Dict[str, Any]: A dictionary containing the receipt data with the following keys:
            - receipt_id (str): The unique identifier of the receipt image.
            - store_name (str): The name of the store.
            - transaction_time (str): The time of purchase in UTC.
            - total_amount (float): The total amount spent.
            - currency (str): The currency of the transaction.
            - purchased_items (List[Dict[str, Any]]): List of items purchased with their details.
        Returns an empty dictionary if no receipt is found.
    """
    # In case of it provide full image placeholder, extract the id string
    image_id = sanitize_image_id(image_id)

    # Query the receipts collection for documents with matching receipt_id (image_id)
    # Notes that this demo assume 1 user only,
    # need to refactor the query for multiple user
    query = COLLECTION.where(filter=FieldFilter("receipt_id", "==", image_id)).limit(1)
    docs = list(query.stream())

    if not docs:
        return {}

    # Get the first matching document
    doc_data = docs[0].to_dict()
    doc_data.pop(EMBEDDING_FIELD_NAME, None)

    return doc_data


def search_by_category(
    category: str,
    start_time: str = "",
    end_time: str = "",
    user_id: str = "default_user"
) -> str:
    """
    Search for expenses in a specific category within a date range.
    
    Args:
        category (str): The category to search for (e.g., "Groceries", "Entertainment").
        start_time (str, optional): The start datetime for the filter in ISO format.
        end_time (str, optional): The end datetime for the filter in ISO format.
        user_id (str, optional): The user identifier for the receipts. Defaults to "default_user".
        
    Returns:
        str: A formatted string containing the results of the search.
    """
    try:
        # Input validation
        if not category:
            raise ValueError("Category must be specified")
            
        # Initialize query
        query = COLLECTION
        
        # Filter by user
        if user_id:
            query = query.where(filter=FieldFilter("user_id", "==", user_id))
        
        # Add date filters if provided
        filters = []
        if start_time:
            try:
                datetime.datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                filters.append(FieldFilter("transaction_time", ">=", start_time))
            except ValueError:
                raise ValueError("start_time must be in ISO format")
                
        if end_time:
            try:
                datetime.datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                filters.append(FieldFilter("transaction_time", "<=", end_time))
            except ValueError:
                raise ValueError("end_time must be in ISO format")
        
        # Apply date filters if any
        if filters:
            composite_filter = And(filters=filters)
            query = query.where(filter=composite_filter)
            
        # Get results
        results = []
        category_total = 0.0
        
        for doc in query.stream():
            data = doc.to_dict()
            
            # Check for items with matching category
            if "purchased_items" in data:
                matching_items = [
                    item for item in data["purchased_items"] 
                    if "category" in item and item["category"].lower() == category.lower()
                ]
                
                if matching_items:
                    # Calculate total for matching items
                    category_amount = sum(item["price"] * item.get("quantity", 1) for item in matching_items)
                    category_total += category_amount
                    
                    # Add to results
                    results.append({
                        "store_name": data["store_name"],
                        "transaction_time": data["transaction_time"],
                        "category_amount": category_amount,
                        "items": [f"{item['name']} (${item['price']})" for item in matching_items]
                    })
        
        # Format results
        if not results:
            return f"No expenses found in category '{category}' for the specified time period."
            
        response = f"Expenses in category '{category}':\n\n"
        for item in results:
            response += f"Store: {item['store_name']}\n"
            response += f"Date: {item['transaction_time']}\n"
            response += f"Amount: ${item['category_amount']:.2f}\n"
            response += f"Items: {', '.join(item['items'])}\n\n"
            
        response += f"Total spent on {category}: ${category_total:.2f}"
        return response
        
    except Exception as e:
        raise Exception(f"Error searching by category: {str(e)}")


def get_category_summary(
    start_time: str = "",
    end_time: str = "",
    user_id: str = "default_user"
) -> str:
    """
    Get a summary of spending by category within a date range.
    
    Args:
        start_time (str, optional): The start datetime for the filter in ISO format.
            If empty, defaults to the beginning of the current month.
        end_time (str, optional): The end datetime for the filter in ISO format.
            If empty, defaults to the current date and time.
        user_id (str, optional): The user identifier for the receipts. Defaults to "default_user".
        
    Returns:
        str: A formatted string containing the spending summary by category.
    """
    try:
        # Initialize query
        query = COLLECTION
        
        # Set default time range to current month if not provided
        if not start_time or not end_time:
            now = datetime.datetime.now()
            
            # If start_time is not provided, use beginning of current month
            if not start_time:
                start_of_month = datetime.datetime(now.year, now.month, 1)
                start_time = start_of_month.isoformat() + "Z"
                logger.info(f"No start time provided, using start of current month: {start_time}")
            
            # If end_time is not provided, use current date and time
            if not end_time:
                end_time = now.isoformat() + "Z"
                logger.info(f"No end time provided, using current time: {end_time}")
        
        # Filter by user
        if user_id:
            query = query.where(filter=FieldFilter("user_id", "==", user_id))
        
        # Add date filters if provided
        filters = []
        if start_time:
            try:
                datetime.datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                filters.append(FieldFilter("transaction_time", ">=", start_time))
            except ValueError:
                raise ValueError("start_time must be in ISO format")
                
        if end_time:
            try:
                datetime.datetime.fromisoformat(end_time.replace("Z", "+00:00"))
                filters.append(FieldFilter("transaction_time", "<=", end_time))
            except ValueError:
                raise ValueError("end_time must be in ISO format")
        
        # Apply date filters if any
        if filters:
            composite_filter = And(filters=filters)
            query = query.where(filter=composite_filter)
            
        # Get results and calculate totals by category
        category_totals = {}
        grand_total = 0.0
        receipt_count = 0
        
        # Debug log for query execution
        logger.info(f"Executing category summary query with date range: {start_time} to {end_time}")
        
        for doc in query.stream():
            receipt_count += 1
            data = doc.to_dict()
            logger.info(f"Processing receipt: {data.get('receipt_id')}")
            
            # Process items with categories
            if "purchased_items" in data:
                item_count = len(data["purchased_items"])
                categorized_items = 0
                
                for item in data["purchased_items"]:
                    if "category" in item:
                        categorized_items += 1
                        category = item["category"]
                        price = item.get("price", 0.0)
                        quantity = item.get("quantity", 1)
                        amount = price * quantity
                        
                        if category not in category_totals:
                            category_totals[category] = 0.0
                            
                        category_totals[category] += amount
                        grand_total += amount
                
                logger.info(f"Receipt has {item_count} items, {categorized_items} have categories")
        
        # Log query results
        logger.info(f"Query returned {receipt_count} receipts with {len(category_totals)} categories")
        
        # Format results
        if not category_totals:
            time_desc = f"from {start_time} to {end_time}"
            if not start_time and not end_time:
                time_desc = "for all time"
            return f"No categorized expenses found {time_desc}. Make sure your receipts have been properly categorized."
            
        # Sort categories by amount (highest first)
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        # Format the date range for display
        try:
            start_date = datetime.datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            end_date = datetime.datetime.fromisoformat(end_time.replace("Z", "+00:00"))
            date_range = f"{start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}"
        except:
            date_range = f"{start_time} to {end_time}"
        
        response = f"Expense Summary by Category ({date_range}):\n\n"
        
        for category, amount in sorted_categories:
            percentage = (amount / grand_total) * 100 if grand_total > 0 else 0
            response += f"{category}: ${amount:.2f} ({percentage:.1f}%)\n"
            
        response += f"\nTotal Expenses: ${grand_total:.2f}"
        
        return response
        
    except Exception as e:
        logger.error(f"Error generating category summary: {str(e)}")
        raise Exception(f"Error generating category summary: {str(e)}")


def categorize_existing_receipts(user_id: str = "default_user") -> str:
    """
    Add categories to items in existing receipts that don't have categories.
    
    Args:
        user_id (str, optional): The user identifier for the receipts. Defaults to "default_user".
        
    Returns:
        str: A message indicating how many receipts and items were updated.
    """
    try:
        # Get all receipts for the user
        query = COLLECTION
        if user_id:
            query = query.where(filter=FieldFilter("user_id", "==", user_id))
        
        receipt_count = 0
        item_count = 0
        
        for doc in query.stream():
            doc_ref = COLLECTION.document(doc.id)
            data = doc.to_dict()
            updated = False
            
            # Process items without categories
            if "purchased_items" in data:
                updated_items = []
                for item in data["purchased_items"]:
                    # Create a copy of the item to avoid modifying the original
                    updated_item = dict(item)
                    
                    # Add category if missing
                    if "category" not in updated_item or not updated_item["category"]:
                        updated_item["category"] = categorize_item(updated_item["name"])
                        updated = True
                        item_count += 1
                    
                    updated_items.append(updated_item)
            
                # Update document if changes were made
                if updated:
                    doc_ref.update({"purchased_items": updated_items})
                    receipt_count += 1
        
        return f"Successfully categorized {item_count} items across {receipt_count} receipts."
        
    except Exception as e:
        raise Exception(f"Error categorizing existing receipts: {str(e)}")


def add_to_google_wallet(
    receipt_id: str, 
    user_id: str = "default_user"
) -> str:
    """
    Add a receipt to Google Wallet for tracking and easy access.
    
    Args:
        receipt_id (str): The unique identifier of the receipt to add to Google Wallet.
        user_id (str, optional): The user identifier for the receipts. Defaults to "default_user".
        
    Returns:
        str: A success message with confirmation details and a shareable link.
        
    Raises:
        Exception: If the operation fails or the receipt doesn't exist.
    """
    try:
        # Sanitize receipt ID
        receipt_id = sanitize_image_id(receipt_id)
        
        # Get receipt data
        receipt_data = get_receipt_data_by_image_id(receipt_id)
        
        if not receipt_data:
            raise Exception(f"Receipt with ID {receipt_id} not found")
        
        # Import the wallet implementation
        try:
            from google_wallet_implementation import GoogleWalletPassManager
        except ImportError as e:
            logger.error(f"Failed to import GoogleWalletPassManager: {str(e)}")
            raise Exception("Google Wallet integration is not available")
            
        logger.info(f"Adding receipt {receipt_id} to Google Wallet for user {user_id}")
        
        # Extract receipt details for Google Wallet
        store_name = receipt_data.get("store_name", "Unknown Store")
        transaction_time = receipt_data.get("transaction_time", "")
        total_amount = receipt_data.get("total_amount", 0.0)
        currency = receipt_data.get("currency", "USD")
        
        # Format date for display
        try:
            transaction_date = datetime.datetime.fromisoformat(transaction_time.replace("Z", "+00:00"))
            formatted_date = transaction_date.strftime("%B %d, %Y")
        except:
            formatted_date = transaction_time
        
        # Initialize wallet manager
        wallet_manager = GoogleWalletPassManager(
            service_account_file='hack2skill-raseed-7655fd0d36ad.json',
            issuer_id='3388000000022956210'
        )
        
        # Define pass content for a receipt
        pass_data = {
            'cardTitle': {
                'defaultValue': {
                    'language': 'en-US',
                    'value': f'Receipt: {store_name}'
                }
            },
            'textModulesData': [
                {
                    'header': 'Store',
                    'body': store_name,
                    'id': 'store_name'
                },
                {
                    'header': 'Date',
                    'body': formatted_date,
                    'id': 'date'
                },
                {
                    'header': 'Amount',
                    'body': f'{currency} {total_amount:.2f}',
                    'id': 'amount'
                },
                {
                    'header': 'Receipt ID',
                    'body': receipt_id,
                    'id': 'receipt_id'
                }
            ],
            'barcode': {
                'type': 'QR_CODE',
                'value': f'https://expense-assistant.example.com/receipt/{receipt_id}'
            }
        }
        
        # Generate shareable link
        pass_object_id = f'receipt_{receipt_id}'
        share_link = wallet_manager.create_jwt_new_pass(
            'test', 
            pass_object_id, 
            pass_data
        )
        
        if not share_link:
            raise Exception("Failed to generate Google Wallet pass link")
        
        # Return success message with the link
        return f"Receipt added to Google Wallet successfully. You can now access your {store_name} receipt dated {formatted_date} in your Google Wallet app.\n\nTo add to your Google Wallet, use this link: {share_link}"
        
    except Exception as e:
        logger.error(f"Error adding receipt to Google Wallet: {str(e)}")
        raise Exception(f"Failed to add receipt to Google Wallet: {str(e)}")