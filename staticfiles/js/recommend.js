$(document).ready(()=>{
    $('#search_form').on('submit', e => {
        e.preventDefault();

        // let requestValue = encodeURIComponent($('#searchQuery').val());
        let requestValue = $('#searchQuery').val();
        let url = `http://127.0.0.1:8000/recommend/`
        let data_ = JSON.stringify({ 'movie': requestValue});
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
                success : (e)=>{
                    console.log('SUCCESSFUL')
                    //console.log()
                },
                error: (e)=>{
                    console.log(e, data_)
                }
            });

            console.log(requestValue)
        }
    })
});

fetch('http://localhost:8000/recommend/')
.then(e=>{
    e.JSON()
    console.log(e)
    
})
.catch(e=>{
    console.log(e)
})