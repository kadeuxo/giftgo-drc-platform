export function payCDF(amountCDF, productCode) {
  FlutterwaveCheckout({
    public_key: window.FLW_KEY,
    tx_ref: 'giftgo_' + Date.now(),
    amount: amountCDF,
    currency: 'CDF',
    payment_options: 'mobilemoneydr',
    customer: {
      email: 'guest@giftgo.cd',
      name:  'GiftGo Guest',
      phone_number: ''            // FLW collects real number in popup
    },
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
