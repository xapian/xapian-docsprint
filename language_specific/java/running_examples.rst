Since there isn't a standard location to install third-party Java
libraries, you will likely have to set the ``CLASSPATH`` variable
appropriately to indicate that you wish to use the Xapian Java
bindings.

There are two parts to the bindings: a jarfile (``xapian.jar``)
containing the Java classes, and the JNI library (such as
``libxapian_jni.so`` on Linux, or ``libxapian_jni.jnilib`` on macOS)
that connects them to Xapian itself. The easiest way to get this
working is to copy those two files to the top-level directory of this
repository. If you built your own Java bindings, the files will be in
``java/built`` in the bindings source code. Then you can use the
following classpath (if on Linux)::

  xapian.jar:libxapian_jni.so:.

If you set the ``CLASSPATH`` variable to this, then the example
commands will work as shown. For instance, if you're using the
``bash`` shell, you should run the following before any example
commands (again, on Linux)::

  export CLASSPATH=xapian.jar:libxapian_jni.so:.
