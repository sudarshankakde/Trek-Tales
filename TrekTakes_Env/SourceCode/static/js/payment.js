document.getElementById('rzp-button1').onclick = (e) => {
    var options = {
        "key": document.getElementById('Razorpay_ApiKey').value, // Enter the Key ID generated from the Dashboard
        "amount": document.getElementById('amount').value + "00", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
        "currency": "INR",
        "name": "Trek Tales",
        "description": "Payment For " + document.getElementById('Heading').value + "Tour.",
        "image": "https://cdn.razorpay.com/logos/K49WBdzj41SEAR_original.png",
        "order_id": document.getElementById('payment_order_id').value, //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
        "handler": function (response) {
            document.getElementById('razorpay_signature').value = response.razorpay_signature;
            document.getElementById('razorpay_order_id').value = response.razorpay_order_id;
            document.getElementById('razorpay_payment_id').value = response.razorpay_payment_id;
            document.getElementById('Payment_Status').value = "True";
            Swal.fire({
                title: 'Payment Successful',
                icon: 'success',
                html:'Your payment receipt will be emailed to you',
                background: '#1c2331',
                color: '#ffffff',
            }).then((result) => {
                if (result.isConfirmed) {
                    document.getElementById('paymentForm').submit();
                    let timerInterval
                    Swal.fire({
                      title: 'Dont close page',
                      html: 'Redirecting...',
                      timer: 2000,
                      timerProgressBar: false,
                      background: '#1c2331',
                      color: '#ffffff',
                      didOpen: () => {
                        Swal.showLoading()
                      },
                      willClose: () => {
                        clearInterval(timerInterval)
                      }
                    }).then((result) => {
                      /* Read more about handling dismissals below */
                      if (result.dismiss === Swal.DismissReason.timer) {
                        console.log('I was closed by the timer')
                      }
                    })
                }
            })
           
        },
        "prefill": {
            "name": document.getElementById('name').value,
            "email": document.getElementById('email').value,
            "contact": document.getElementById('Phone_no1').value
        },
        "notes": {
            "Tour": document.getElementById('Heading').value,
        },
        "theme": {
            "color": "#498553"
        }
    };
    var rzp1 = new Razorpay(options);
    rzp1.on('payment.failed', function (response) {
        console.error(response.error.code);
        console.error(response.error.description);
        console.error(response.error.source);
        console.error(response.error.step);
        console.error(response.error.reason);
        console.error(response.error.metadata.order_id);
        console.error(response.error.metadata.payment_id);
        var issue = 'response.error.reason'
        Swal.fire({
            title: 'Payment Failed',
            icon: 'error',
            html:`We are sorry, but your payment has failed due to an issue. Please try again`+'<br><small>You will receive a refund within 48-72 hours if any amount has been debited from your account.</small>',
            background: '#1c2331',
            color: '#ffffff',
        }).then((result) => {
            if (result.isConfirmed) {
                
            }
        })
    });

    rzp1.open();
    e.preventDefault();
}
