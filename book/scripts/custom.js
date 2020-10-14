function checkSlideForElement(slide, elem) {
    res = slide.getElementsByTagName("div");
    for (i=0; i<res.length; i++) {
        if (res[i].getAttribute("id") == elem) {
            return true;
        }
    }
    return false;
}
        
function addLectureNumber (lectureNo) {
    var lectureNum = "Lecture." + lectureNo;	
    // applies to all slides
    d3.selectAll("div").filter(".content").append("div").attr("class","task").html(lectureNum);
}

        
function addLectureNumberNew (lectureNo) {
    var lectureNum = "Lecture." + lectureNo;    
    // applies to all slides
    d3.selectAll("div").filter(".remark-slide-content").append("div").attr("class","task").html(lectureNum);
}

function incrementalBulletSlide () {
    remark.emit('pauseRemark');
    
    function getState() {
        mytag = d3.selectAll(".slide")
        .filter(function(d,i) { return this.style.cssText == "display: table; "; })
        .select("input[name='state']");
        
        if( mytag[0][0] == null) {
            setState(0);
            return 0;
        } else {
            return parseInt(mytag.property("value"));  
        } 
    }
    
    function setState(val) {
        d3.selectAll(".slide")
        .filter(function(d,i) { return this.style.cssText == "display: table; "; })
        .select("input[name='state']").remove();

        d3.selectAll(".slide")
        .filter(function(d,i) { return this.style.cssText == "display: table; "; })
        .append("input")
        .attr("type","hidden")
        .attr("name","state")
        .attr("value",val);
    }        
    
    function keydown() {
        console.log("i got the keypress not remark!");
        console.log(state, bullets[0].length);
        switch (d3.event.keyCode) {
            case 39: // right arrow
                if(d3.event.metaKey) return;
            case 40: // down arrow
            case 34: // page down
            case 32: // spacebar
                state += 1;
                if (state>=totalstates) {
                    d3.select(window).on("keydown",null); // remove d3 catches
                    remark.emit("resumeRemark"); // resume remark
                    remark.emit("gotoNextSlide"); // go to next slide
                    return;
                }
                break;
            case 37: // left arrow
                if (d3.event.metaKey) return;
            case 38: // up arrow
            case 33: // page up
                state -= 1;
                if (state<0) {
                    d3.select(window).on("keydown",null); // remove d3 catches
                    remark.emit("resumeRemark"); // resume remark
                    remark.emit("gotoPrevSlide"); // go to previous slide
                    return;                              
                }
            break;
        }
        setState(state);
        update(400);
    }
    
    function update(delay) {
        console.log("updating list", state);
        bullets.transition().duration(delay).style("opacity", function (d,i) {
            if (i<state) return "0.3"
            else if (i==state) return "1.0"
            else if (i>state) return "0.0"
        });
    } 
    
    bullets = d3.selectAll(".slide").filter(function(d,i) { return this.style.cssText == "display: table;"; }).selectAll("li");
    console.log(bullets);
    state = getState();
    totalstates = bullets[0].length;
    update(0);
    d3.select(window).on("keydown", keydown);
    
}
