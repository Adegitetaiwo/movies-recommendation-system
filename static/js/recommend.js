$(document).ready(()=>{
    $('#search_form').on('submit', e => {
        e.preventDefault();

        // let requestValue = encodeURIComponent($('#searchQuery').val());
        let requestValue = $('#searchQuery').val();
        let url = `http://127.0.0.1:8000/recommend/`
        let data_ =  requestValue;
        //if input is empty
        if (!requestValue) {
            console.log('Please Enter Something!')
        } else {

            $.ajax({
                url : url,
                method : 'POST',
                dataType: 'json',
                data: data_,
                beforeSend: ()=>{
                    $('#apiPreloader').show()
                },
                complete: ()=>{
                    $('#apiPreloader').hide()
                },
                success : (success)=>{
                    //console.log(success[1])

                    let loading = `
                    <p style="padding-top:10px; font-weight:bold;">${success.loading_msg_1}</p>
                    <p>Item index in system Database : ${success.msg_if_found +1}</p>
                    <p>${success.loading_msg_2} : <span style="color:green; font-weight:bold;">Done!</span></p>
                    `
                    let output = `
                    <p style="padding-top:10px;">${success[1]}</p><p>${success[2]}</p><p>${success[3]}</p><p>${success[4]}</p><p>${success[5]}</p>
                    <p>${success[6]}</p><p>${success[7]}</p><p>${success[8]}</p><p>${success[9]}</p><p style="padding-buttom:10px;">${success[10]}</p>
                    `
                    if (!output || success[404]==''){
                        document.getElementById('search_form').reset();
                        
                        $('#apiLoading').css('display', 'none');
                        $('#apiResult').css('display', 'none');

                        let resultNotFound = '<p>Awwn, so sorry there is No Database Match, please try something else!</p>'
                        $('#apiResultNotFound').css('display', 'block')
                       $('#apiResultNotFound').html(resultNotFound)
                        $('#apiResultNotFound').css('display', 'block');
                       //console.log(resultNotFound)
                    }else{
                        document.getElementById('search_form').reset();
                    
                        $('#apiResultNotFound').css('display', 'none');
                        $('#apiLoading').html(loading)
                        $('#apiResult').html(output)
                        $('#apiLoading').css('display', 'block');
                        $('#apiResult').css('display', 'block');
                        //apiResult.childNodes(htmlResult)
                        
                        //console.log(output)
                    }
                },
                error: (error)=>{
                    $('#apiResultNotFound').html(`<p>Internal server Error!</p>`)
                    console.log(error)
                }
            });

        }
    })
});