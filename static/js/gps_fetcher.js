const container = document.body;

function fetch_gps()
{
  const latinput = document.getElementById('latinput');
  const longinput = document.getElementById('longinput');
  if(document.getElementById('latlong_gps').checked) {
    if ("geolocation" in navigator)
    {
      navigator.geolocation.getCurrentPosition((position) => {
        latinput.value = position.coords.latitude;
        longinput.value = position.coords.longitude;
        console.log(position.coords.latitude, position.coords.longitude);
      });
    }
    else
    {
      console.log("Failed to fetch GPS!");
    }
    disable_input();
  }
}

function enable_input()
{
  const latinput = document.getElementById('latinput');
  const latlabel = document.getElementById('latlabel');
  const longinput = document.getElementById('longinput');
  const longlabel = document.getElementById('longlabel');
  latinput.readonly = false;
  latinput.style.visibility = "visible";
  longinput.readonly = false;
  longinput.style.visibility = "visible";

  latlabel.style.visibility = "visible";
  longlabel.style.visibility = "visible";
}

function disable_input()
{
  const latinput = document.getElementById('latinput');
  const latlabel = document.getElementById('latlabel');
  const longinput = document.getElementById('longinput');
  const longlabel = document.getElementById('longlabel');
  latinput.readonly = true;
  latinput.style.visibility = "visible";
  longinput.readonly = true;
  longinput.style.visibility = "visible";
  latlabel.style.visibility = "visible";
  longlabel.style.visibility = "visible";
}

function hide_input()
{
  const latinput = document.getElementById('latinput');
  const latlabel = document.getElementById('latlabel');
  const longinput = document.getElementById('longinput');
  const longlabel = document.getElementById('longlabel');
  latinput.style.visibility = "hidden";
  longinput.style.visibility = "hidden";
  latlabel.style.visibility = "hidden";
  longlabel.style.visibility = "hidden";
}