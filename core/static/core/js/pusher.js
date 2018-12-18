var PushBack = {
    _app_key : null,
    _client_id : null,
    _chatSocket:null,

    init: function(app_key, client_id){
        this._app_key = app_key;
        this._client_id = client_id
    },

    subscribe: function(onNotification, onClose){
        this._chatSocket = new WebSocket(
        'wss://' + window.location.host +
        '/ws/notifications/subscribe/'+this._app_key+'/'+ this._client_id +'/');

        this._chatSocket.onmessage = onNotification

        this._chatSocket.onclose = onClose
    }
}
