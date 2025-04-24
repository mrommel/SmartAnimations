import * as THREE from 'three';
import Stats from './jsm/libs/stats.module.js';
import { OrbitControls } from './jsm/controls/OrbitControls.js'
import { InteractionManager } from "./thirdparty/three.interactive.js";
import * as TWEEN from "./thirdparty/tween.esm.js";

var scene, camera, renderer, stats, controls, interactionManager;
var meshFloor;

var keyboard = {};
var player = { height: 1.8, speed: 0.1, turnSpeed: Math.PI*0.01 };
var USE_WIREFRAME = false;
var plane;

var cx, cz;

function createCube({ color, x, y }) {
    const geometry = new THREE.BoxGeometry(0.5, 0.5, 0.5);
    const material = new THREE.MeshLambertMaterial({ color });
    const cube = new THREE.Mesh(geometry, material);
    cube.position.set(x, y, 0);

    return cube;
}

const capture = () => {
    const canvas = document.querySelector('#container canvas');
    if (canvas) {
        const base64 = canvas.toDataURL('img/png');
        // document.querySelector('#img').src = base64;
        // console.log('write image to server');
    } else {
        console.log('cannot find canvas');
    }
};

const container = document.getElementById('container');

var cameraParams = {
    near: 0.1,
    far: 1000.0,
    fov: 90,                    // degrees?!
    aspectRatio: window.innerWidth / window.innerHeight,       // from the dimensions of the canvas. see CSS
    atX: 0,
    atY: 1.8,
    atZ: 12,
    eyeX: 0,  // cx
    eyeY: 0,
    eyeZ: 25,  // cz
    upX: 0,
    upY: 1,
    upZ: 0
};

// global, so we can modify it from the GUI
var camera = new THREE.PerspectiveCamera();

// globals, modified from the above
var at  = new THREE.Vector3();  // lookAt
var eye = new THREE.Vector3();
var up  = new THREE.Vector3();

function setCameraView() {
    at.set(cameraParams.atX, cameraParams.atY, cameraParams.atZ);
    eye.set(cameraParams.eyeX, cameraParams.eyeY, cameraParams.eyeZ);
    up.set(cameraParams.upX, cameraParams.upY, cameraParams.upZ);
}
setCameraView();

function setupCamera(scene) {
    // camera shape
    var fov    = cameraParams.fov || 90;  // in degrees
    var aspect = cameraParams.aspectRatio || window.innerWidth / window.innerHeight;  // canvas width/height
    var near   = cameraParams.near || 0.1;  // measured from eye
    var far    = cameraParams.far  || 1000.0;  // measured from eye
    camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
    // camera location
    setCameraView();
    camera.position.copy(eye);
    // Cameras inherit an "up" vector from Object3D.
    camera.up.copy(up);
    camera.lookAt(at);
    return camera;
}

function adjustCamera() {
    // the following are for the camera shape
    camera.fov    = cameraParams.fov;
    camera.aspect = cameraParams.aspectRatio;
    camera.near   = cameraParams.near;
    camera.far    = cameraParams.far;
    // to account for the settings above
    camera.updateProjectionMatrix();
    // camera location
    camera.position.copy(eye);
    camera.up.copy(up);  // Cameras inherit an "up" vector from Object3D.
    camera.lookAt(at);
}

function init() {
	scene = new THREE.Scene();
    scene.add(new THREE.AxesHelper(5));  // shows the axis cross
    setupCamera(scene);

    const light = new THREE.PointLight(0xffffff, 2);
    light.position.set(0, 5, 10);
    scene.add(light);

    renderer = new THREE.WebGLRenderer({
        antialias: true,
        preserveDrawingBuffer: true,
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);
    // controls.enableDamping = true;

    controls.addEventListener("change", event => {
        cameraParams.atX = controls.target.x;
        cameraParams.atY = controls.target.y;
        cameraParams.atZ = controls.target.z;
        cameraParams.eyeX = controls.object.position.x;
        cameraParams.eyeY = controls.object.position.y;
        cameraParams.eyeZ = controls.object.position.z;
        setCameraView();
    });

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

    interactionManager = new InteractionManager(
        renderer,
        camera,
        renderer.domElement
    );

    // objects
    const cubes = {
        pink: createCube({ color: 0xff00ce, x: -3, y: 0, z: 1 }),
        purple: createCube({ color: 0x9300fb, x: 3, y: 0, z: 1 }),
        blue: createCube({ color: 0x0065d9, x: 1, y: 0, z: 1 }),
        cyan: createCube({ color: 0x00d7d0, x: -1, y: 0, z: 1 })
    };

    for (const [name, object] of Object.entries(cubes)) {
        object.addEventListener("click", (event) => {
            event.stopPropagation();
            console.log(`${name} cube was clicked`);

            const cube = event.target;
            const coords = { x: camera.position.x, y: 5, z: camera.position.z };
            new TWEEN.Tween(coords)
                .to({ x: cube.position.x, y: 5, z: cube.position.z })
                .onUpdate(() =>
                    camera.position.set(coords.x, camera.position.y, coords.z)
                )
                .start();
        });
        interactionManager.add(object);
        scene.add(object);
    }

    var gui = new dat.GUI();
    gui.add(cameraParams, 'fov', 1, 179).onChange(onCameraParamsChange).listen();
    gui.add(cameraParams, 'eyeX', 1, 179).onChange(onCameraParamsChange).listen();
    gui.add(cameraParams, 'eyeY', 1, 179).onChange(onCameraParamsChange).listen();
    gui.add(cameraParams, 'eyeZ', 1, 179).onChange(onCameraParamsChange).listen();

    animate();
}

function onCameraParamsChange() {
    setCameraView();
    adjustCamera();
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;  // fixme
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    animate();
}

function animate(time) {
	requestAnimationFrame(animate);
	
	// Keyboard movement inputs
	if(keyboard[87]) { // F key
		cameraParams.atX -= player.speed * 10;
		onCameraParamsChange();
	}
	if(keyboard[83]) { // S key
		cameraParams.atX += player.speed * 10;
		onCameraParamsChange();
	}
	if(keyboard[65]) { // A key
		cameraParams.eyeX += Math.sin(camera.rotation.y + Math.PI/2) * player.speed;
		cameraParams.eyeZ += -Math.cos(camera.rotation.y + Math.PI/2) * player.speed;
		onCameraParamsChange();
	}
	if(keyboard[68]) { // D key
		cameraParams.eyeX += Math.sin(camera.rotation.y - Math.PI/2) * player.speed;
		cameraParams.eyeZ += -Math.cos(camera.rotation.y - Math.PI/2) * player.speed;
		onCameraParamsChange();
	}
	
	// Keyboard turn inputs
	if(keyboard[37]) { // left arrow key
		camera.rotation.y -= player.turnSpeed;
		onCameraParamsChange();
	}
	if(keyboard[39]) { // right arrow key
		camera.rotation.y += player.turnSpeed;
		onCameraParamsChange();
	}

	controls.update();
	
	renderer.render(scene, camera);

	capture();

	interactionManager.update();
    TWEEN.update(time);

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