var btnSave = document.getElementById('btn-save');
var btnDel = document.getElementById('del-all');

var chbNotCall = document.getElementById('checkbox1');
var chbIReadIt = document.getElementById('checkbox2');
var chbIDontChoose = document.getElementById("checkbox3");
var chbIConfirm = document.getElementById('checkbox4');
var chbImOver = document.getElementById("checkbox5");
var chbThisTask = document.getElementById('checkbox6');

if (getCookie('poll')) { //if the poll on this page has already taken place
  setCondition(chbNotCall);
  setCondition(chbIReadIt);
  setCondition(chbIDontChoose);
  setCondition(chbIConfirm);
  setCondition(chbImOver);
  setCondition(chbThisTask);

  btnSave.disabled = true;
}

btnSave.addEventListener('click', async _ => {
  date = getLifetime();

  setCookie('poll', 1, {
    expires: date,
  })

  saveState(chbNotCall);
  saveState(chbIReadIt);
  saveState(chbIDontChoose);
  saveState(chbIConfirm);
  saveState(chbImOver);
  saveState(chbThisTask);

  btnSave.disabled = true;
});

btnDel.addEventListener('click', async _ => {
  deleteAllCookies();
});

function setCondition(name) {
  //This function restores condition of checkboxes on startup p
  var temp = document.getElementById(name.id);
  if (getCookie(name.id) == 1) {
    temp.checked = true;
  }
  temp.disabled = true;
}

function getLifetime() {
  let date = new Date(Date.now() + 86400e3); //the lifetime of cookies one day
  return date.toUTCString();
}

function saveState(name) { //accepts a variable with the checkbox as an argument
  //This function saves the state using coockies
  date = getLifetime();

  if (name.checked) {
    let nameCookie = name.id;
    setCookie(nameCookie, 1, {
      expires: date
    })
  } else {
    let nameCookie = name.id;
    setCookie(nameCookie, 0, {
      expires: date
    })
  }

  name.disabled = true;
}

function deleteAllCookies() {
  //This function delete all cookies and make all checkboxes is unchecked
  document.cookie.split(";").forEach(function (c) {
    document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/");
  });

  chbNotCall.checked = false;
  chbIReadIt.checked = false;
  chbIDontChoose.checked = false;
  chbIConfirm.checked = false;
  chbImOver.checked = false;
  chbThisTask.checked = false;

  btnSave.disabled = false;
}

if (getCookie('city')) {
  console.log('block undefined')
  let inp = document.getElementById('input-city');
  inp.remove();

  let p = document.createElement('p');
  p.innerHTML = 'Ваш город — ' + getCookie('city');
  document.body.append(p);

  let btnRem = document.createElement('button');
  btnRem.innerHTML = 'Удалить город';
  document.body.append(btnRem);

  btnRem.addEventListener('click', async _ => {
    deleteCookie('city');
  });
} else {
  console.log('block defined')

  let inp = document.getElementById('input-city');
  inp.oninput = () => {
    setCookie('city', inp.value, {
      'max-age': 3600 // cookie live 10 min
    })
  };
}

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options = {}) {
  //This function set cookie
  options = {
    path: '/',
    ...options
  };

  if (options.expires.toUTCString) {
    options.expires = options.expires.toUTCString();
  }

  let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
  for (let optionKey in options) {
    updatedCookie += "; " + optionKey;
    let optionValue = options[optionKey];
    if (optionValue !== true) {
      updatedCookie += "=" + optionValue;
    }
  }
  document.cookie = updatedCookie;
}

function deleteCookie(name) {
  setCookie(name, "", {
    'max-age': -1
  })
} 