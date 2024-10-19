
    document.addEventListener('DOMContentLoaded', ()=> {


      // Use buttons to toggle between views
    document.querySelector('.allpost').addEventListener('click', () => load_posts('all posts', 1));
    document.querySelector('.following').addEventListener('click', () => load_posts('following', 1));


    load_posts('all posts');

    document.querySelector('#posts').addEventListener('click', (event) => {
        if (event.target.classList.contains('likeunlike')) {
            likeunlike(event.target);
        }
    });


    document.querySelector('#posts').addEventListener('click', (event) => {
        if (event.target.classList.contains('username')) {
            profile(event.target);
        }
    });

    document.querySelector('#profile').addEventListener('click', (event) => {
        if (event.target.classList.contains('followunfollow')) {
            followunfollow(event.target);
        }
    });








})


function load_posts(constraint, page){
    document.querySelector('#profile').style.display = 'none';
    document.querySelector('#form').style.display = 'none';
    document.querySelector('#posts').style.display = 'block';
    document.querySelector('#posts').innerHTML = '';



    document.querySelector('#heading').innerHTML = constraint.toUpperCase();


    let url;
    if (constraint == 'all posts') {
        url = `/posts?page=${page}`;
    } else {
        url = `/posts/following?page=${page}`;
    }
    console.log(url)
    fetch(url, {
        method: "GET",
    })
    .then(response => response.json())
    .then(response => {
        console.log(response.posts);
        response.posts.forEach(post => {

        view_post(post)

        
        });

        document.querySelector('#pagination-controls').innerHTML = '';

        nav = loadnav(constraint, response, response.page);
        console.log(response.has_next)
        document.querySelector('#pagination-controls').appendChild(nav)
        
    });

    
}


function view_post(post) {
    parent = document.createElement('div');
    parent.classList.add('card');

    var childElement = document.createElement('p');
    childElement.textContent = post.user.username;
    console.log(post.user.username);
    childElement.classList.add('card-header', 'username')
    childElement.setAttribute('data-user-id', post.user.id);

    parent.appendChild(childElement);

    var subparent = document.createElement('div')
    subparent.classList.add('card-body')

    var childElementcon = document.createElement('p');
    childElementcon.textContent = post.content;
    childElementcon.classList.add('card-title', 'textarea', 'thecontent');
    subparent.appendChild(childElementcon);
    console.log(post.content);

    var childElementb = document.createElement('button');
    childElementb.classList.add('likeunlike')
    console.log('/likeunlike'+post.id);
    fetch('/likeunlike/'+post.id).then(response => response.json())
    .then(response => {
        if (response.liked == true){
            childElementb.innerHTML = 'Unlike';
            childElementb.classList.add('unlike','likeunlike')
            childElementb.setAttribute('data-post-id', post.id);
            subparent.appendChild(childElementb);
            console.log(post.likes);
        }else{
            childElementb.innerHTML = 'Like';
            childElementb.classList.add('like', 'likeunlike')
            subparent.appendChild(childElementb);
            childElementb.setAttribute('data-post-id', post.id);

            console.log(post.likes);
        }
        console.log(post.my);
        if(post.my){

            var button = document.createElement('button');
            button.innerHTML = 'Edit';
            button.classList.add('editbtn')
            subparent.appendChild(button);
            button.addEventListener('click', () => edit(post, button, childElementcon));
        }
        
    })


    var childElement = document.createElement('p');
    childElement.textContent = post.likes;
    childElement.setAttribute('data-like-id', post.id);

    childElement.classList.add('card-text', 'like-count')
    subparent.appendChild(childElement);
    console.log(post.likes);



    parent.appendChild(subparent)

    document.querySelector('#posts').append(parent);
}


function likeunlike(button) {
    console.log("likeunlike")
    const postid = button.getAttribute('data-post-id');
    fetch("/likeunlike/"+postid, {
        "method": "POST"
    })
    .then(response => response.json())
    .then(response => {
        if (response.liked == true){
            button.innerHTML = 'Unlike';
        }else{
            button.innerHTML = 'Like';
        }
        document.querySelector(`[data-like-id='${postid}']`).innerHTML = response.count;
        
    })
}


function profile(button) {
    const userid = button.getAttribute('data-user-id');
    // console.log(userid)
    username = button.innerHTML;
    console.log(username);
    fetch('/profile/'+username).then(response => response.json())
    .then(response => {
        document.querySelector('#profile').style.display = 'block';
        document.querySelector('#form').style.display = 'none';
        // document.querySelector('#posts').style.display = 'none';
        document.querySelector('#profile').innerHTML = '';

        document.querySelector('#heading').innerHTML = username;


        box = document.querySelector('#profile')


        followers = document.createElement('p');
        followers.innerHTML = `Followers: ${response.followers}`;
        followers.classList.add('followernumber');

        box.appendChild(followers)

        following = document.createElement('p');
        following.innerHTML = `Followings: ${response.followings}`;
        box.appendChild(following)


        
        var childElementb = document.createElement('button');
        childElementb.classList.add('followunfollow');
        fetch('/followunfollow/'+userid).then(response => response.json())
        .then(response => {
            console.log(response)
            if (response.follow == true){
                childElementb.innerHTML = 'Unfollow';
                childElementb.classList.add('unfollow','followunfollow')
                childElementb.setAttribute('data-followee-id', response.followeeid);
                box.appendChild(childElementb);
            }else if (response.follow == false){
                childElementb.innerHTML = 'Follow';
                childElementb.classList.add('follow', 'followunfollow')
                box.appendChild(childElementb);
                childElementb.setAttribute('data-followee-id', response.followeeid);
            }

        })

    })
    url = "/posts/"+username
    fetch(url, {
        method: "GET",  
        'page' :"1"
    })
    .then(response => response.json())
    .then(response => {
        document.querySelector('#posts').style.display = 'block';
        document.querySelector('#posts').innerHTML = '';
        console.log(response.posts);
        response.posts.forEach(post => {

            view_post(post)
        });
    });
}


function followunfollow(button){
    const followeeid = button.getAttribute('data-followee-id');
    fetch('/followunfollow/'+followeeid , {
        "method" : "POST"
    }).then(response => response.json())
    .then(response => {
        if (response.follow == false) {
            button.innerHTML = 'Follow';
            following = document.querySelector('.followernumber');
            following.innerHTML = `Followers: ${response.count}`;

        }else{
            button.innerHTML = 'Unfollow';
            following = document.querySelector('.followernumber');
            following.innerHTML = `Followers: ${response.count}`;

        }
    })

}


function loadnav(constraint, response, page){
    nav = document.createElement('nav');
    nav.setAttribute('aria-label', '...');
    ul = document.createElement('ul');
    ul.classList.add('pagination');

    if (response.has_previous){
        li = document.createElement('li');
        li.classList.add('page-item');
        span = document.createElement('span')
        span.classList.add('page-link');
        span.innerHTML = 'Previous';
        li.appendChild(span);
        ul.appendChild(li);
        li.addEventListener('click', () => pageclick(page, 'prev', constraint))
    }

    if (response.has_next){
        li = document.createElement('li');
        li.classList.add('page-item');
        span = document.createElement('span')
        span.classList.add('page-link');
        span.innerHTML = 'Next';
        li.appendChild(span);
        ul.appendChild(li);
        li.addEventListener('click', () => pageclick(page, 'next', constraint))
    }

    nav.appendChild(ul);
    return nav
}


function pageclick(page, str, constraint){
    let newpage;
    if(str == 'prev'){
        console.log('page number' + page);
        console.log('new page number' + newpage);

        newpage = page - 1;
    }else{
        newpage = page + 1;
        console.log('page number' + page);
        console.log('new page number' + newpage);


    }
    load_posts(constraint, newpage)
}


function edit(post, button, childElementcon){
    console.log('/n/n/n/n/n/n editttttttttttttttttttttttttt');
    let textarea = document.createElement('textarea');
    textarea.textContent = post.content;
    button.parentNode.appendChild(textarea);
    button.style.display = 'none';

    let btnSave = document.createElement('button');
    btnSave.innerHTML = 'Save';
    button.parentNode.appendChild(btnSave);

    console.log('Button Parent Node:', button.parentNode);
    console.log('btnSave:', btnSave);

    btnSave.addEventListener('click', () => editpost(post, textarea, btnSave, childElementcon, button));

}


function editpost(post, textarea, btnSave, childElementcon, button){
    url = '/edit/'+post.id;
    fetch(url, {
        "method": "POST",
        body: JSON.stringify({ "content": textarea.value })
    })
    .then(response => response.json())
    .then(response => {
        if (response.success){
            
        
            textarea.remove();
            btnSave.remove();
            childElementcon.textContent = response.content;
            button.style.display = 'inline';


        }
    })
}