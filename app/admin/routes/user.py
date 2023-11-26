from datetime import datetime as dt

from sqlalchemy import bindparam, and_
from north_admin import (
    FilterGroup,
    Filter,
    FieldType,
    AdminRouter,
    AdminMethods,
)

from app.models.user import User


user_get_columns = [
    User.id,
    User.email,
    User.fullname,
    User.user_type,
    User.created_at,
]


router = AdminRouter(
    model=User,
    model_title='Users',
    enabled_methods=[
        AdminMethods.GET_ONE,
        AdminMethods.GET_LIST,
        AdminMethods.SOFT_DELETE,
    ],
    pkey_column=User.id,
    soft_delete_column=User.is_active,
    get_columns=user_get_columns,
    list_columns=user_get_columns,
    filters=[
        FilterGroup(
            query=(
                and_(
                    User.created_at > dt.now().replace(hour=0, minute=0, second=0),
                    bindparam('created_today_param'),
                )
            ),
            filters=[
                Filter(
                    bindparam='created_today_param',
                    title='Created today',
                    field_type=FieldType.BOOLEAN,
                ),
            ],
        ),
        FilterGroup(
            query=(User.created_at > bindparam('created_after_gt')),
            filters=[
                Filter(
                    bindparam='created_after_gt',
                    title='Created after',
                    field_type=FieldType.DATETIME,
                )
            ],
        ),
    ]
)