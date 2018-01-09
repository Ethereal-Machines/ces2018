/*
 * (c) Kanishka Mohan Madhuni (kmmadhuni@gmail.com)
 */

/* Using Module-reveal Design Pattern for Javascript */
; (function ($, ethrealStore, window, document, undefined) {
  var SuccessModal = ethrealStore.SuccessModal = ethrealStore.SuccessModal || (function() {

    /* All the variables of the module go here */
    // var modalOpenButton = $('.btn--modal');
    var modalCloseButton = $('.btn--close-modal');
    var successModal = $('.success-modal');
    var form = $('.user-form');
    /* Fields to show the errors */
    var errorFields = $('.field-error-msg');
    var nameError = $('#name-error');
    var emailError = $('#email-error');
    var cellphoneError = $('#cellphone-error');
    var addressError = $('#address-error');
    // var recaptchaError = $('#captcha-error');

    var errorMsg = $('.error-msg');
    var loadingAnimation = $('.loading-animation');
    var submitBtn = $('#submit-btn');
    var formData = {};

    /* Function to register the events on the different elements */
    function event(item, event, callback) {
      item.on(event, function(){
        callback();
      });
    }

    /* Registering the events */
    // event(modalOpenButton, 'click', openModal);
    event(modalCloseButton, 'click', closeModal);
    event(submitBtn, 'click', submitForm);

    /* Private methods go here */
    function submitForm() {
      errorMsg.text('').addClass('hide');
      submitBtn.addClass('hide');
      loadingAnimation.removeClass('hide');
      var serializedData = form.serializeArray();
      serializedData.forEach(function (element) {
        formData[element.name] = element.value;
      });
      console.log(formData);

      $.ajax({
        url: '/',
        type: 'POST',
        data: JSON.stringify(formData),
        dataType: 'json',
        contentType: "application/json; charset=utf-8",
        beforeSend: function(request) {
          request.setRequestHeader("X-CSRF-Token", formData['csrf_token']);
        },
        success: function() {
          errorMsg.text("");
          errorMsg.addClass('hide');
          form[0].reset();
          reset();
          openModal();
        },
        error: function(xhr) {
          errorMsg.removeClass('hide');
          errorMsg.text('Please fill in all the details to claim your coupon.');
          /* Removing all the other error messages */
          errorFields.text("");
          reset();

          var errorData = xhr.responseJSON.error_fields;
          var html = `<sup>* </sup>`;
          if (errorData !== undefined) {
            for (var element in errorData) {
              if (element === 'name') {
                var msg = errorData[element][0];
                nameError.html(html + msg);
              } else if (element === 'email') {
                var msg = errorData[element][0];
                emailError.html(html + msg);
              } else if (element === 'cellphone') {
                var msg = errorData[element][0];
                cellphoneError.html(html + msg);
              } else if (element === 'address') {
                var msg = errorData[element][0];
                addressError.html(html + msg);
              } 
              /* Corresponds to captcha code */
              // else if (element === 'recaptcha') {
              //   var msg =  errorData[element][0];
              //   recaptchaError.html(html + msg);
              // }
            }
          }
          console.log(xhr);
        }
      });
    }

    function reset() {
      loadingAnimation.addClass('hide');
      submitBtn.removeClass('hide');
    }
    
    /* Public methods go here */
    function openModal() {
      console.log('fun is running');
      var modal = $('.success-modal');
      modal.removeClass('hide');
    }

    function closeModal() {
      var modal = $('.success-modal');
      modal.addClass('hide');
    }

    /* Returning the object with the public method */
    return {
      closeModal: closeModal
    };


  })();
}(jQuery, window.ethrealStore = window.ethrealStore || {}, window, document));
