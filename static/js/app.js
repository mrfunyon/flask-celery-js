$(document).ready(function(){
    var timeoutfuncs = {};
    function checkStatus(tid, el){
        $.ajax({
            url: "/check/work/" + tid,
        }).done(function(data){
            if (data['status'] == 'ready'){
                el.text = "Result is: " + data['result'];
                clearInterval(timeoutfuncs[tid]);
                delete timeoutfuncs[tid];
                console.log(timeoutfuncs);
            }
        });
    }
    $('a.async').click(function(e) {
        e.preventDefault();
        this.text="Sending Work...";
        el = this;
        $.ajax({
            async: true,
            url: el.href,
        }).done(function(data){
            el.text="Awaiting Answer...";
            timeoutfuncs[data['task_id']] = setInterval(checkStatus, 1000, data['task_id'], el);
        });
    });
    // $('a.send-work').click(function(e) {
    //     e.preventDefault();
    //     this.text="Sending Work...";
    //     $.ajax({
    //         async: false,
    //         url: "/send/work/",
    //     }).done(function(data){
    //         $.ajax({
    //             async: false,
    //             url: "/check/work/" + data['task_id'] + "/f",
    //         }).done(function(data){
    //             $('a.send-work')[0].text="Result is: " + data['result'];
    //         });
    //     });
    // });
});