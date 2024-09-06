
// get search form and page links
let search_form = document.getElementById('search_form');
let page_links = document.getElementsByClassName('btn page-link');

console.log(search_form, page_links);
// ensure search form exists
if(search_form){
console.log('inside if')
for(let i=0; i < page_links.length; i++){
    
    page_links[i].addEventListener('click', function(e){
    e.preventDefault() //stops pagination default to next page
    console.log('Button clicked');
    // get the page data attribute
    let page_num = this.dataset.page_num;
    console.log(page_num);

    // add hidden search input
    search_form.innerHTML+= `<input value=${page_num} name='page' hidden/>`

    // submit form
    search_form.submit()
    // this way instead of page_num to go to next page,
    // we're submitting the search form with page num. 
    // check how this is query efficient 
    })
}
}

// remove tags when editing project 
// get the tags
let tags = document.getElementsByClassName('project-tag');
console.log(tags)

// add event listeners to tags
for (let i=0; i<tags.length; i++){
    tags[i].addEventListener('click', (e) =>{
        // get clicked ids of tag/project
        let tag_id = e.target.dataset.tag
        let project_id = e.target.dataset.project
        console.log('tag id',tag_id, project_id)

        fetch('http://127.0.0.1:8000/api/remove-tag/', {
            method:'DELETE',
            headers:{
                'Content-type':'application/json'
            },
            body:JSON.stringify({'project_id':project_id, 
                                    'tag_id':tag_id})
        })
        .then(response => response.json())
        .then(data => {
            e.target.remove()
        })
    })
}
