document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#read-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#compose-form').onsubmit = () => {
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      })
    })
      .then(response => response.json())
      .then(() => {
        load_mailbox('sent');
      }); 

    return false;
  };
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#read-email').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
    .then(emails =>{
      for(let email of emails){
        if(email.archived && mailbox == inbox){
          //pass
        }
        else{
          const emaildiv = document.createElement('div')
          emaildiv.setAttribute('class',"border border-secondary mt-2")
          email.read? emaildiv.style.backgroundColor = "grey":emaildiv.style.backgroundColor="white";
          emaildiv.innerHTML += "From: " + email.sender + "<br />";
          emaildiv.innerHTML += "Subject: "+ email.subject + "<br/>";
          emaildiv.innerHTML += email.timestamp + "<br/>"; 
          document.querySelector('#emails-view').appendChild(emaildiv);
          emaildiv.addEventListener('click', ()=> load_email(email));

          if(mailbox != 'sent'){
            const archive = document.createElement('button');
            archive.setAttribute("class","btn-btn-danger");
            archive.textContent = email.archived ? "Unarchive" : "archive";
            document.querySelector('#emails-view').appendChild(archive);
            archive.addEventListener('click',() => {
              fetch('/emails/'+`${email.id}`,{
                method:'PUT',
                body:JSON.stringify({
                  archived:!(email.archived)
                })
              }).then(() => load_mailbox(mailbox));
            });

          }
        }
      }
    });
  }

  function load_email(email){
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#read-email').style.display = 'block';

    fetch('/emails/'+`${email.id}`)
    .then(response => response.json())
    .then(email => {
      document.querySelector('#read-email').innerHTML = `<h3>${email.subject}</h3>`

      const emaildiv = document.createElement('div');
      emaildiv.setAttribute("class","border mt-2")
      emaildiv.innerHTML += "From: " + email.sender + "<br/>";
      emaildiv.innerHTML += "subject: " + email.subject + "<br/>";
      emaildiv.innerHTML +="recipients: ";
      for(let recipient of email.recipients){
        emaildiv.innerHTML += recipient;
      }
      emaildiv.innerHTML += "<br />";
      emaildiv.innerHTML += "send on " + email.timestamp + "<br/>";
      emaildiv.innerHTML += "<br/>";
      emaildiv.innerHTML += email.body;
      document.querySelector('#read-email').appendChild(emaildiv);

      const reply = document.createElement('button');
      reply.setAttribute("class","btn btn-primary");
      reply.textContent = "Reply";
      document.querySelector('#read-email').appendChild(reply);

      reply.addEventListener('click', ()=>{
         compose_email();

         document.querySelector('#compose-recipients').value = email.sender;
         document.querySelector('#compose-subject').value = email.subject;
         document.querySelector('#compose-body').value =  email.body +  ' ' + "sent on" + email.timestamp ;
      });
    });
    fetch('/emails/'+`${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    });
  }
