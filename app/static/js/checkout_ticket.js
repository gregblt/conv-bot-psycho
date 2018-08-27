$(function() {
  $('button#try-code').click(function() {
    console.log($('#promo-code').val())
    if($('#promo-code').val()!='') {
      $.ajax({
              url: '/promo_code',
              type: 'GET',
              data:{
                'code':$('#promo-code').val()
              },
              contentType: 'application/json; charset=utf-8',
              dataType: 'json',
              success: function(response) {
                console.log(response);
                if(response.total_entries==0) {
                  $('<div id="promo-error" style="color:red;"> Promo code invalid or does not exist</div>').insertBefore("#promo-code-div")
                }
                else {
                  $('#promo-error').remove()
                  promo_code=response.promotion_codes[0]              
                  if(promo_code.percentage) {
                    discount=subtotal*(promo_code.value/100)                                   
                    $('#discount').replaceWith('<div class="cart-text" id="discount"">Discount: <b>-$'+discount.toFixed(2)+' ('+promo_code.value+'%</b> with promo code <b>'+promo_code.code+')</b> </div>')
                    
                  }
                  else {
                    discount=promo_code.value                                
                    $('#discount').replaceWith('<div class="cart-text" id="discount"">Discount: <b>-$'+promo_code.value.toFixed(2)+'</b> with promo code <b>'+promo_code.code+'</b> </div>')
                  }
                  total=subtotal+delivery-discount+service;
                  $('#total').html( "<b> Total: $"+ total.toFixed(2) +"</b>")
                }
              }
          });
    }
  });
});

cardFormCallback = function(result){
console.log(result);
var $inputs = $('form :input');
  console.log($inputs)
  console.log('ouistiti')
  console.log(result)
  error=false;

  if('error' in result){
    error=true;
  }
  token=result

  var values = {};
  $inputs.each(function() {
      values[this.name] = $(this).val();
      console.log(this.name+', val:'+values[this.name])

    if(this.name=='email'){
      var input=$('input[name=email]');
      var re = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
      var is_email=re.test(input.val());
      if(is_email){input.removeClass("invalid").addClass("valid");}
      else{input.removeClass("valid").addClass("invalid");error=true;}
    }
    else if(this.name=='full-name') {
      var input=$('input[name=full-name]');
      var re = /^(([A-Za-z]+[\-\']?)*([A-Za-z]+)?\s)+([A-Za-z]+[\-\']?)*([A-Za-z]+)?$/;
      var is_email=re.test(input.val());
      if(is_email){input.removeClass("invalid").addClass("valid");}
      else{input.removeClass("valid").addClass("invalid");error=true;}
    }
    else if(this.name=='street-address') {
      var input=$('input[name=street-address]');
      var re = /^(([A-Za-z]+[\-\']?)*([A-Za-z]+)?\s)+([A-Za-z]+[\-\']?)*([A-Za-z]+)?$/;
      if(input.val()) {
        input.removeClass("invalid").addClass("valid");
      }
      else {
        input.removeClass("valid").addClass("invalid");error=true;
      }
    }
    else if(this.name=='city') {
      var input=$('input[name=city]');
      var re = /^(([A-Za-z]+[\-\']?)*([A-Za-z]+)?\s)+([A-Za-z]+[\-\']?)*([A-Za-z]+)?$/;
      if(input.val()) {
        input.removeClass("invalid").addClass("valid");
      }
      else {
        input.removeClass("valid").addClass("invalid");error=true;
      }
    }
    else if(this.name=='state') {
      var input=$('input[name=state]');
      if(input.val()) {
        input.removeClass("invalid").addClass("valid");
      }
      else {
        input.removeClass("valid").addClass("invalid");error=true;
      }
    }
    else if(this.name=='zip') {
      var input=$('input[name=zip]');
      if(input.val()) {
        input.removeClass("invalid").addClass("valid");
      }
      else {
        input.removeClass("valid").addClass("invalid");error=true;
      }

    }
      console.log(error)


    

  });
    data={
      'full-name':$('input[name=full-name]').val(),
      'street-address':$('input[name=street-address]').val(),
      'state':$('input[name=state]').val(),
      'city':$('input[name=city]').val(),
      'zip':$('input[name=zip]').val(),
      'country':$('select[name=country]').val(),
      'email':$('input[name=email]').val(),
      'phone-number':$('input[name=phone-number]').val(),
      'phone-country-code':$('input[name=phone-country-code]').val(),
      'ticket-group-id':$("meta[name=ticket-group-id]").attr("content")
    }


    
    console.log(data)

    if(error){
      console.log('error');
    }
    else {
      console.log('processing...')

      $.ajax({
        url: '/create_client_eticket',
        type: 'POST',
        data:JSON.stringify({
          'data':data
        }),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        success: function(response) {
          console.log(response);
          $( "#delivery" ).replaceWith( response.html );
          delivery = JSON.parse(response.json).price
          client=response.client

          total=subtotal+delivery-discount+service;
          $('#delivery-fee').html( 'Delivery fee: <b>$'+ delivery.toFixed(2) +'</b>')
          $('#total').html( '<b>Total: $'+ total.toFixed(2) +'</b>')
          $('#spinner').replaceWith('<button type="submit" class="tevo-stripe-button">Save Card Information</button>')
        }
    });  
  }
}

//tevoStripe = TevoStripe('stripeContainer', cardFormCallback, {production: false,submitText:'Payment',hidePhoneField:true,hideCityField:true,hideAddressField:true});
tevoStripe = TevoStripe('stripeContainer', cardFormCallback,{production: false,hidePhoneField:true,hideCityField:true,hideAddressField:true});

document.addEventListener("DOMContentLoaded", function(event) {
tevoStripe.mount();
})

