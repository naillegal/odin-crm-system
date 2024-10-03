$(document).ready(function () {
  $('.clicktodown').on('click', function () {
      $(this).next('#dropdown-feedback').slideToggle(300); 
      $('.clicktodown').not(this).each(function () {
          $(this).next('#dropdown-feedback').slideUp(300); 
      });
  });

  $('.clicktodowncrud').on('click', function () {
    $(this).next('#dropdown-crud').slideToggle(300); 
    $('.clicktodowncrud').not(this).each(function () {
        $(this).next('#dropdown-crud').slideUp(300); 
    });
});

  $('.box').each(function () {
      const box = $(this); 
      const feedButton = box.find('.feed');
      const infoButton = box.find('.info');
      const feedTab = box.find('.tab1');
      const infoTab = box.find('.tab2');

      feedTab.show();
      infoTab.hide();
      feedButton.addClass('active');

      feedButton.on('click', function () {
          feedTab.show();
          infoTab.hide();
          feedButton.addClass('active');
          infoButton.removeClass('active');
      });

      infoButton.on('click', function () {
          feedTab.hide();
          infoTab.show();
          infoButton.addClass('active');
          feedButton.removeClass('active');
      });
  });
});
