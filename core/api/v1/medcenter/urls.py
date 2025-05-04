from ninja import Router

from core.api.v1.medcenter.handlers import (
    router_appointment,
    router_doctor,
    router_doctor_schedule,
    router_person,
    router_schedule,
    router_specialization,
    router_ticket,
    router_waiting_list,
)


router = Router(tags=["medcenter"])

router.add_router("doctor/", router_doctor)
router.add_router("person/", router_person)
router.add_router("specialization/", router_specialization)
router.add_router("appointment/", router_appointment)
router.add_router("ticket/", router_ticket)
router.add_router("schedule/", router_schedule)
router.add_router("doctor_schedule/", router_doctor_schedule)
router.add_router("waiting_list/", router_waiting_list)
