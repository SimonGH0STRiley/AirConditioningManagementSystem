let mysql  = require('mysql');

let connection = mysql.createConnection({
    host     : '103.105.49.174:3306',
    user     : 'root',
    password : 'some_pass',
    // TODO: 2 Be Done
    database : 'test_AirConditioningManagementSystem'
});



// 查询房间状态
function queryRoomStatus (targetRoom) {
    // 使用Promise更改异步操作为同步操np作，使得回调函数能正确执行
    let promise = new Promise( (resolve, reject) => {
        // 建立连接
        connection.connect(function (error) {
            if (error) {
                reject('[CONNECT ERROR] - ' + error.stack);
            }
            console.log('[CONNECT SUCCESS] - Connected as id ' + connection.threadId);
        });

        let querySql = 'SELECT * FROM room WHERE room_no = ?';
        let querySqlParams = [targetRoom];
        connection.query(querySql, querySqlParams, function (error, result) {
            if (error) {
                reject('[SELECT ERROR] - ' + error.message);
            }
            resolve(result);
        });

        // 终止连接
        connection.end();
    });

    promise.then(data => {
        console.log(data);
        return data;
    }).catch(res => {
        console.log(res);
        return 0;
    });
    return promise;
}

// 更改房间状态
function updateRoomStatus (targetRoom, targetTemperature, currTemperature) {
    // 使用Promise更改异步操作为同步操作，使得回调函数能正确执行
    let promise = new Promise(function (resolve, reject) {
        // 建立连接
        connection.connect(function (error) {
            if (error) {
                reject('[CONNECT ERROR] - ' + error.stack);
            }
            console.log('[CONNECT SUCCESS] - Connected as id ' + connection.threadId);
        });

        let modSql = 'UPDATE test SET targetTemperature = ?, currTemperature = ? WHERE channel_no = ?';
        let modSqlParams = [targetTemperature, currTemperature, targetRoom];

        connection.query(modSql, modSqlParams,function (error, result) {
            if(error){
                reject('[UPDATE ERROR] - ' + error.message);
            }
            resolve(result);
        });

        // 终止连接
        connection.end();
    });

    promise.then(data => {
        console.log(data);
        return data;
    }).catch(res => {
        console.log(res);
        return 0;
    });
    return promise;
}

function calRoomACFee (targetRoom) {
    // TODO: discuss about it
}

module.exports = {queryRoomStatus, updateRoomStatus};
