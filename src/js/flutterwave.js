export function payCDF(amountCDF, productCode) {
    FlutterwaveCheckout({
      public_key: window.FLW_KEY,
      tx_ref: 'giftgo_' + Date.now(),
      amount: amountCDF,
      currency: 'CDF',
      payment_options: 'mobilemoneydr',          // Airtel + M‑Pesa
      customer: { phone_number: '' },            // FLW prompts user
      callback: data => {
        if (data.status === 'successful') {
          fetch('/.netlify/functions/afterPayment', {
            method: 'POST',
            body: JSON.stringify({ data, productCode })
          });
        } else {
          alert('Paiement annulé.');
        }
      },
      onclose: () => console.log('checkout closed')
    });
  }
  