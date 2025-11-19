const projectsEle = document.querySelector('#project-list');
const guidesEle = document.querySelector('#guide-list');
const projectsEle = document.querySelector('#fun-list');

projectsFileName = './endpoints.json'

function addProjects(list) {
  const docfrag = document.createDocumentFragment();
  list.forEach((i) => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = "." + i.sitename;
    li.classList.add('subsite');
    const span = document.createElement('span');
    const favplacehold = document.createElement('span');
    favplacehold.classList.add('favico');
    const favico = document.createElement('img');
    favico.src = i.favicon;
    favplacehold.appendChild(favico);
    span.classList.add('site-name');
    span.innerText = list.title;
    a.appendChild(span);
    a.appendChild(favplacehold);
    li.appendChild(a);
    docfrag.appendChild(li);
  });
  return docfrag;
}

if (projectsEle) {
  fetch(projectsFileName)
    .then(response => {
      if (!response.ok) { throw new Error('HTTP error' + response.status);}
      return response.json();
    }).then(projectsFile => {
      projectsEle.appendChild(addProjects(projectsFile['sites']))
    }).catch(error => console.error('Error fetching JSON:', error));
}
