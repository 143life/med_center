from ninja import Router

from core.api.v1.medcenter.urls import router as medcenter_router


router = Router(tags=["v1"])
router.add_router("medcenter/", medcenter_router)
