A async aliyun OSS library
===========================

Based on https://github.com/aliyun/aliyun-oss-python-sdk

文档参考官方文档, 调用io操作的接口前加await即可

.. code-block:: python

    result = await bucket.get_object(...
    
获取返回内容::

    body = await result.resp.read()


Getting started
----------------

.. code-block:: python

    # -*- coding: utf-8 -*-

    import aiooss

    endpoint = 'http://oss-cn-hangzhou.aliyuncs.com' # Suppose that your bucket is in the Hangzhou region.

    auth = aiooss.Auth('<Your AccessKeyID>', '<Your AccessKeySecret>')

    async def go(loop):
        # The object key in the bucket is story.txt
        async with aiooss.Bucket(auth, endpoint, '<your bucket name>') as bucket:
            key = 'story.txt'

            # Upload
            await bucket.put_object(key, 'Ali Baba is a happy youth.')
            
            # Upload
            data = dict(a=1, b=2)
            await bucket.put_object(key, json.dumps(data), headers={'Content-Type': 'application/json'})

            # Download
            result = await bucket.get_object(key)
            print(result.headers)
            print(await result.resp.read())

            # Delete
            await bucket.delete_object(key)

            # Traverse all objects in the bucket
            async for object_info in aiooss.ObjectIterator(bucket):
                print(object_info.key)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(go(loop))
