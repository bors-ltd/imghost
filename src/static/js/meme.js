jQuery(function($) {
    var form = $('#meme-form');
    var topInput = $('#top-text');
    var bottomInput = $('#bottom-text');
    var imgCanvas = $('#meme-canvas');
    var ctx = imgCanvas[0].getContext("2d");
    var img = $('#meme-image');
    var imgWidth, imgHeight;

    var initialize = function() {
        imgWidth = img.width();
        imgHeight = img.height();
        imgCanvas.attr('width', imgWidth);
        imgCanvas.attr('height', imgHeight);

        $.extend(ctx, {
            strokeStyle : '#000000',
            textAlign : 'center',
            fillStyle : '#ffffff',
            lineCap : 'round'
        });

        updateMeme();
    };

    var writeTopCaption = function(text) {
        ctx.textBaseline = 'top';
        writeCaption(text, 5);
    };

    var writeBottomCaption = function(text) {
        ctx.textBaseline = 'bottom';
        writeCaption(text, imgHeight - 5);
    };

    var writeCaption = function(text, y) {
        var size = parseInt(imgWidth / 5);

        do {
            ctx.font = size + 'px Impact';
            ctx.lineWidth = size / 32;
            size--;
        } while(ctx.measureText(text).width >= imgWidth - 40);

        ctx.fillText(text, imgWidth / 2, y);
        ctx.strokeText(text, imgWidth / 2, y);
    };

    var updateMeme = function() {
        var topText = topInput.val();
        var bottomText = bottomInput.val();

        ctx.clearRect(0, 0, imgWidth, imgHeight);
        ctx.drawImage(img[0], 0, 0);

        writeTopCaption(topText);
        writeBottomCaption(bottomText);
    };

    initialize();
    form.on('keyup', updateMeme);
});
