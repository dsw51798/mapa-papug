import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const degToRad = (deg) => (deg * Math.PI) / 180;

const container = document.body;
//const width = .666*container.clientWidth;
//console.log("Width: "+container.clientWidth+", Height: "+container.clientHeight+" Sum: "+(container.clientWidth/container.clientHeight));
if((window.innerWidth / window.innerHeight) > 1.5){
  var width = .333*container.clientWidth;
}
else
{
  var width = .666* container.clientWidth;
}

window.addEventListener('resize', () => {
    if((window.innerWidth / window.innerHeight) > 1.5)
  {
    var width = .333*container.clientWidth;
  }
  else
  {
    var width = .666* container.clientWidth;
  }

    renderer.setSize(width, width);
    camera.aspect = 1;
    camera.updateProjectionMatrix();
});

container.addEventListener("scroll", (event) => {
  console.log(container.scrollTop);
});

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87ceeb);
const camera = new THREE.PerspectiveCamera( 60, 1, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( width, width );
renderer.setAnimationLoop( animate );
//document.body.appendChild( renderer.domElement );
document.querySelector('#render_container').appendChild( renderer.domElement );

const controls = new OrbitControls( camera, renderer.domElement );
controls.target.set( 0, 0, 0 )
controls.enableDamping = true;
controls.dampingFactor = 0.1;
controls.enableZoom = false;

const color = 0xFFFFFF;
const light = new THREE.AmbientLight(color, 3);
scene.add(light);

const sphereGeometry = new THREE.SphereGeometry( 2, 64, 32 );
const material = new THREE.MeshStandardMaterial( {
  color: 0xffffff,
  map: new THREE.TextureLoader().load('/static/img/tex/map_color_dim.png'),
  metallic: 0,
  roughness: 1
} );
const sphere = new THREE.Mesh( sphereGeometry, material );
scene.add( sphere );
sphere.material.shading = THREE.FlatShading;
//sphere.geometry.computeVertexNormals(true);

camera.position.z = 5;
camera.position.x = 0;
light.position.z = 5;
light.position.x = 0;

async function loadPhotos() {
  const response = await fetch('/static/live/photos.json');
  const photos = await response.json();
  addMarkers(photos);
}

//"Come on, do some of that pilot stuff!" - Goose, Top Gun (1986)
function addMarkers(photos) {
  photos.forEach(({ lat, lon, photo }) => {
    const latRad = degToRad(lat);
    const lonRad = degToRad(-lon);
  
    const x = 2.05 * Math.cos(latRad) * Math.cos(lonRad);
    const y = 2.05 * Math.sin(latRad);
    const z = 2.05 * Math.cos(latRad) * Math.sin(lonRad);
  
    const markerGeometry = new THREE.SphereGeometry(0.05, 8, 4);
    const markerMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000 });
    const marker = new THREE.Mesh(markerGeometry, markerMaterial);
    marker.material.shading = THREE.FlatShading;
    marker.geometry.computeVertexNormals(true);

    marker.userData = {photo: photo};
    marker.name = "photoMarker";
  
    marker.position.set(x, y, z);
    scene.add(marker);
  });
}

loadPhotos();

const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();
const popup = document.getElementById("map_popup");

var activeMarker = null;
var activeMarkerSavedPosition = null;
var popupOffset = null;
const popupSize = new THREE.Vector2(parseInt(getComputedStyle(popup).width), parseInt(getComputedStyle(popup).height));

window.addEventListener('click', (event) => {
  let canvasBounds = renderer.getContext().canvas.getBoundingClientRect();
  pointer.x = ((event.clientX - canvasBounds.left) / (canvasBounds.right - canvasBounds.left)) * 2 - 1;
  pointer.y = - ((event.clientY - canvasBounds.top) / (canvasBounds.bottom - canvasBounds.top)) * 2 + 1;

  raycaster.setFromCamera(pointer, camera);
  //console.log(pointer);

  // Get the list of intersected objects
  const intersects = raycaster.intersectObjects(scene.children);

  if (intersects.length > 0) {
    //console.log(intersects);
    const object = intersects[0].object;
    if(object.name == "photoMarker")
    {
      if(activeMarker != null) activeMarker.material.color.set(0xff0000);
      activeMarker = object;
      const photo = document.getElementById("map_image");
      
      object.material.color.set(0x00ff00);
      //console.log(object.userData.photo);
      
      popup.style.visibility = 'visible';

      //console.log(popupSize.x);
      popupOffset = new THREE.Vector2((event.clientX - popupSize.x/2) / window.innerWidth, (event.clientY - popupSize.y*1.1 + window.scrollY) / window.innerHeight);

      //console.log("Adjusting popup by a scroll val of "+window.scrollY)
      //console.log(popupOffset);
      popup.style.left = ''+100*(popupOffset.x)+'%'
      popup.style.top = ''+100*(popupOffset.y)+'%'

      photo.src = "/static/live/src/"+object.userData.photo;
      console.log(object.userData.photo);
    }
  else
    {
      if(activeMarker != null)
      {
        activeMarker.material.color.set(0xff0000);
        activeMarker = null;

        popup.style.visibility = 'hidden';
      }
    }
  }
});


function animate() {
  requestAnimationFrame(animate);

  if(activeMarker != null && popup.style.visibility == 'visible')
  {
    camera.updateMatrixWorld();
    //console.log(activeMarker.position.project(camera));

    //popup.style.left = ''+100*(activeMarker.position.project(camera).x)+'%'
    //popup.style.top = ''+100*(activeMarker.position.project(camera).y)+'%'
  }

  controls.update();
  renderer.render( scene, camera );
}