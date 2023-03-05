import Stats from './stats.module.js';

var scene, camera, renderer, stats;
var meshFloor;

var keyboard = {};
var player = { height: 1.8, speed: 0.1, turnSpeed: Math.PI*0.01 };
var USE_WIREFRAME = false;
export var plane;

function init() {
	scene = new THREE.Scene();
    // scene.add(new THREE.AxesHelper(5));

    const light = new THREE.PointLight(0xffffff, 2);
    light.position.set(0, 5, 10);
    scene.add(light);

    camera = new THREE.PerspectiveCamera(
        90,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    // camera.position.z = 12.0;
    camera.position.set(0, player.height, 12);
	camera.lookAt(new THREE.Vector3(0,player.height,0));

    renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

	// Texture Loading
	var textureLoader = new THREE.TextureLoader();
	
	// const planeGeometry = new THREE.PlaneGeometry(3.6, 1.8)
	const planeGeometry = new THREE.PlaneGeometry(40, 20, 10,10);
    const material = new THREE.MeshPhongMaterial();

    const texture = textureLoader.load('/static/animations/img/textures/worldColour.4096x2048.png');
    material.map = texture;

    const normalTexture = textureLoader.load('/static/animations/img/textures/earth_normalmap_8192x4096.jpg');
    material.normalMap = normalTexture;
    material.normalScale.set(2, 2);

    const bumpTexture = new THREE.TextureLoader().load('/static/animations/img/textures/earth_bumpmap.jpg');
    material.bumpMap = bumpTexture;
    material.bumpScale = 0.015;

    plane = new THREE.Mesh(planeGeometry, material);
    plane.rotation.x -= Math.PI / 2;
    scene.add(plane);

	window.addEventListener('resize', onWindowResize, false);

    stats = Stats();
    document.body.appendChild(stats.dom);

    animate();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    animate();
}

function animate() {
	requestAnimationFrame(animate);
	
	// mesh.rotation.x += 0.01;
	// mesh.rotation.y += 0.02;
	
	// Keyboard movement inputs
	if(keyboard[87]){ // W key
		camera.position.x -= Math.sin(camera.rotation.y) * player.speed;
		camera.position.z -= -Math.cos(camera.rotation.y) * player.speed;
	}
	if(keyboard[83]){ // S key
		camera.position.x += Math.sin(camera.rotation.y) * player.speed;
		camera.position.z += -Math.cos(camera.rotation.y) * player.speed;
	}
	if(keyboard[65]){ // A key
		// Redirect motion by 90 degrees
		camera.position.x += Math.sin(camera.rotation.y + Math.PI/2) * player.speed;
		camera.position.z += -Math.cos(camera.rotation.y + Math.PI/2) * player.speed;
	}
	if(keyboard[68]){ // D key
		camera.position.x += Math.sin(camera.rotation.y - Math.PI/2) * player.speed;
		camera.position.z += -Math.cos(camera.rotation.y - Math.PI/2) * player.speed;
	}
	
	// Keyboard turn inputs
	if(keyboard[37]){ // left arrow key
		camera.rotation.y -= player.turnSpeed;
	}
	if(keyboard[39]){ // right arrow key
		camera.rotation.y += player.turnSpeed;
	}
	
	renderer.render(scene, camera);
	stats.update();
}

function keyDown(event) {
	keyboard[event.keyCode] = true;
}

function keyUp(event) {
	keyboard[event.keyCode] = false;
}

function toggleWireframe() {
    // mesh.material.wireframe=!mesh.material.wireframe;
    // meshFloor.material.wireframe=!meshFloor.material.wireframe;
    plane.material.wireframe=!plane.material.wireframe;
}

window.addEventListener('keydown', keyDown);
window.addEventListener('keyup', keyUp);

window.onload = init;

window.toggleWireframe = toggleWireframe;