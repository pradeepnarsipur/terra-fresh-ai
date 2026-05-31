from services.supabase_service import supabase


def create_seller_supabase(
    full_name,
    business_name,
    whatsapp,
    city,
    password_hash
):

    data = {
        "full_name": full_name,
        "business_name": business_name,
        "whatsapp": whatsapp,
        "city": city,
        "password_hash": password_hash
    }

    response = (
        supabase
        .table("sellers")
        .insert(data)
        .execute()
    )

    return response


def get_seller_by_whatsapp_supabase(whatsapp):

    response = (
        supabase
        .table("sellers")
        .select("*")
        .eq("whatsapp", whatsapp)
        .execute()
    )

    if len(response.data) == 0:
        return None

    return response.data[0]


def create_product_supabase(
    seller_id,
    product_name,
    category,
    price,
    quantity,
    description
):

    data = {
        "seller_id": seller_id,
        "product_name": product_name,
        "category": category,
        "price": price,
        "quantity": quantity,
        "description": description
    }

    response = (
        supabase
        .table("products")
        .insert(data)
        .execute()
    )

    return response


def get_all_products_supabase():

    response = (
        supabase
        .table("products")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


def get_seller_by_id_supabase(seller_id):

    response = (
        supabase
        .table("sellers")
        .select("*")
        .eq("id", seller_id)
        .execute()
    )

    if len(response.data) == 0:
        return None

    return response.data[0]