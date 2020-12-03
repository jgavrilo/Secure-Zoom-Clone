const socket = io('/')
const videoGrid = document.getElementById('video-grid')
const myVideo = document.createElement('video')
let myPeer = null

myVideo.muted = true
let peers = {}

navigator.mediaDevices.getUserMedia({
    video: true,
    audio: true
    }).then(stream => {
        myPeer = new Peer(undefined, {
            host: '/',
            port: '3001'
            })
        addVideoStream(myVideo, stream)
        myPeer.on('open', id => {
            socket.emit('join-room', ROOM_ID, id)
            })
        myPeer.on('call', call => {
            call.answer(stream)
            const video = document.createElement('video')
            call.on('stream', userVideoStream => {
                addVideoStream(video, userVideoStream)
                })
            })

        socket.on('user-connected', userId => {
            console.log("new user connected", userId)
            connectToNewUser(userId, stream)
            })

    }).catch(error=>{
        console.log("Error: ",error)
        })

socket.on('user-disconnected', userId => {
    if (peers[userId]) peers[userId].close()
    })

function connectToNewUser(userId, stream) {
    const call = myPeer.call(userId, stream)
    const video = document.createElement('video')
    call.on('stream', userVideoStream => {
        addVideoStream(video, userVideoStream)
        })
    call.on('close', () => {
    video.remove()
    })

    peers[userId] = call
    console.log(peers)
}

function addVideoStream(video, stream) {
    video.srcObject = stream
    video.addEventListener('loadedmetadata', () => {
        video.play()
        })
    videoGrid.append(video)
    }