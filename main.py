import uvicorn



if __name__ == '__main__':
    uvicorn.run('lib:app', host='0.0.0.0', port=1210, access_log=True)