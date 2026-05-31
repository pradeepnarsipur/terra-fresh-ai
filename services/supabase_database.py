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

    return response