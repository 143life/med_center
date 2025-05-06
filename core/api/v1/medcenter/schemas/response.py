from pydantic import BaseModel

from core.api.v1.medcenter.schemas.ticket import TicketSchema


class AppointmentOut(BaseModel):
    specialization: str
    completed: bool


class TicketOut(BaseModel):
    ticket: "TicketSchema"
    appointments: list["AppointmentOut"]

    @staticmethod
    def from_ticket_and_appointment_out(
        ticket: TicketSchema,
        appointment_out_list: list[AppointmentOut],
    ) -> "TicketOut":
        return TicketOut(ticket=ticket, appointments=appointment_out_list)
