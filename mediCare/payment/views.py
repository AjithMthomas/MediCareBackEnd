import json
import razorpay
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . models import Appointment
from datetime import date
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Order,Appointment
from .serializers import Appointmentserializer
from accounts.models import User
from datetime import datetime
from Doctors.models import Doctors,Slots
from rest_framework import status



class AppointmentListView(ListAPIView):
    serializer_class = Appointmentserializer
    def get_queryset(self):
        return Appointment.objects.all()




class DoctorAppointmentsAPIView(APIView):
    def get(self, request,id):
        try:
            # doctor = Doctors.objects.filter(doctor=id)
            appointments = Appointment.objects.filter(doctor=id)
            serializer = Appointmentserializer(appointments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response("Appointments not found", status=status.HTTP_404_NOT_FOUND)



class start_payment(APIView):
    def post(self, request, format=None):
        
        amount = request.data['amount']
        current_user = request.data['user']
        print(current_user,'ojsoigjsdgjsajjojijfsifas')
        user = User.objects.get(id=current_user)

        doc = request.data['doctor']
        print(doc)
        doctor = Doctors.objects.get(id=doc)

        slot = request.data['slot']
        print(slot)
        current_slot = Slots.objects.get(id=slot)

        PUBLIC_KEY = 'rzp_test_GrC2fomAR5BvCu'
        SECRET_KEY = 'K3oUpvscgHYIteoxLW3u0Quf'

        # setup razorpay client this is the client to whome user is paying money that's you
        client = razorpay.Client(auth=(PUBLIC_KEY,SECRET_KEY))


        payment = client.order.create({"amount": int(amount) * 100, 
                                    "currency": "INR", 
                                    "payment_capture": "1"})
        
        
      

        order = Appointment.objects.create(
                                    patient = user,
                                    appointment_payment_id = payment['id'],
                                    order_date = datetime.now().date(),
                                    doctor = doctor,
                                    slot = current_slot,
                                   )

        serializer = Appointmentserializer(order)
       
        data = {
            "payment": payment,
            "order": serializer.data
        }
        return Response(data)



class handle_payment_success(APIView):
    def post(self, request, format=None):
        res = json.loads(request.data["response"])
        slot = request.data['slot']
       


        ord_id = ""
        raz_pay_id = ""
        raz_signature = ""

        # res.keys() will give us list of keys in res
        for key in res.keys():
            if key == 'razorpay_order_id':
                ord_id = res[key]
            elif key == 'razorpay_payment_id':
                raz_pay_id = res[key]
            elif key == 'razorpay_signature':
                raz_signature = res[key]

        order = Appointment.objects.get(appointment_payment_id=ord_id)

        data = {
            'razorpay_order_id': ord_id,
            'razorpay_payment_id': raz_pay_id,
            'razorpay_signature': raz_signature
        }

        PUBLIC_KEY = 'rzp_test_GrC2fomAR5BvCu'
        SECRET_KEY = 'K3oUpvscgHYIteoxLW3u0Quf'
        
        client = razorpay.Client(auth=(PUBLIC_KEY, SECRET_KEY))

        check = client.utility.verify_payment_signature(data)


        order.isPaid = True
        order.save()
        slot = Slots.objects.get(id=slot)
        slot.is_booked = True
        slot.save()
    
     
        res_data = {
            'message': 'payment successfully received!',
            'order_id' : ord_id
        }

        return Response(res_data)