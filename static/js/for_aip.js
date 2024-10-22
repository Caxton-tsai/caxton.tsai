/*!
* Start Bootstrap - Resume v7.0.6 (https://startbootstrap.com/theme/resume)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-resume/blob/master/LICENSE)
*/
//
// Scripts
// 

let images = {}


window.addEventListener('DOMContentLoaded', event => {

    // Activate Bootstrap scrollspy on the main nav element
    const sideNav = document.body.querySelector('#sideNav');
    if (sideNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#sideNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

    document.addEventListener('DOMContentLoaded', function() {
        const uploadForm = document.getElementById('uploadForm');
    
        uploadForm.addEventListener('submit', function(event) {
            event.preventDefault(); // 阻止表單的默認提交行為
            console.log("Form submission prevented");
            uploadFile(event);
        });
    });

    // Upload file function
    const uploadFile = function() {
        event.preventDefault();
        const formData = new FormData(document.getElementById('uploadForm'));
        fetch('/for_load_img', {
            method: 'POST',
            body: formData,
        })
        .then(response =>  response.json())
        .then(data => {
            if (data) {
                const imageUrl = `${data.gray}?v=${Date.now()}`;
                document.getElementById('selectedImage').src = imageUrl;
            } 
            
        })
    };
   
        // Function to update image source
    window.updateImage = function(filterType) {
        event.preventDefault();
        const formData = new FormData();
        formData.append('updatetype',filterType)
        fetch('/for_load_aip_img',{
            method:'POST',
            body: formData
        })
        .then(response =>  response.json())
        .then(data => {
            if (data) {
                const imageUrl = `${data[filterType]}?v=${Date.now()}`;
                document.getElementById('additionalImage').src = imageUrl;
                
            } 
        })
        // const imgSrc = images[filterType];
        // var baseUrl = "/img/";
        // var imgSrc = "";
        // switch (filterType) {
        //     case 'histogram':
        //         imgSrc = baseUrl + "histogram_01.webp";
        //         break;
        //     case 'gaussian':
        //         imgSrc = baseUrl + "gaussian.jpg";
        //         break;
        //     case 'haar':
        //         imgSrc = baseUrl + "haar.jpg";
        //         break;
        //     case 'equalization':
        //         imgSrc = baseUrl + "equalization.jpg";
        //         break;
        //     default:
        //         alert("Unknown filter type");
        //         return;
        // }

        // document.getElementById('additionalImage').src = imgSrc;
    };

    // Add event listeners to buttons
    // document.querySelector('button[onclick="updateImage(\'histogram\')"]').addEventListener('click', function() {
    //     updateImage('histogram');
    // });
    // document.querySelector('button[onclick="updateImage(\'gaussian_noise\')"]').addEventListener('click', function() {
    //     updateImage('gaussian');
    // });
    // document.querySelector('button[onclick="updateImage(\'haar\')"]').addEventListener('click', function() {
    //     updateImage('haar');
    // });
    // document.querySelector('button[onclick="updateImage(\'equalization\')"]').addEventListener('click', function() {
    //     updateImage('equalization');
    // });
    document.querySelector('.submit').addEventListener('click', uploadFile);

});
