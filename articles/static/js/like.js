const likeButtons = document.querySelectorAll('.likeButtons')
 likeButtons.forEach( likeButton =>{

 likeButton.addEventListener('click', event => {
    const articleID =event.target.dataset.id
    {% if user.is_authenticated %}
        axios.get(`/articles/${articleID}/like/`)
        .then( response => {
            likeCount = response.data.count
            console.log('???', likeCount)
            if (likeCount == 0){
              likeCount = document.querySelector(`#likeCount-${articleID}`).classList.add('d-none')
              firstLiker = document.querySelector(`#firstLiker-${articleID}`).classList.add('d-none')
            }else if (likeCount == 1){
              likeCount = document.querySelector(`#likeCount-${articleID}`).classList.add('d-none')
              firstLiker = document.querySelector(`#firstLiker-${articleID}`)
              firstLiker.innerText = 'Liked by ' + response.data.first
              firstLiker.classList.remove('d-none')
            }else {
              firstLiker = document.querySelector(`#firstLiker-${articleID}`)
              firstLiker.innerText = 'Liked by ' + response.data.first
              firstLiker.classList.remove('d-none')
              likeCount = document.querySelector(`#likeCount-${articleID}`)
              likeCount.classList.remove('d-none')
              likeCount.innerText = ' and ' + (response.data.count -1) + ' others'
            }

            if (response.data.liked){
                event.target.classList.remove('far', 'animated', 'infinite', 'bounce', 'slow', 'delay-1s')
                event.target.classList.add('fas')
            }
            else {
                event.target.classList.remove('fas')
                event.target.classList.add('far', 'animated', 'infinite', 'bounce', 'slow', 'delay-1s')
            }
        })
    {% else %}
        alert('Please login!')
    {% endif %}
    })
})