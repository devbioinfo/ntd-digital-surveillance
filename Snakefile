rule hello:
    output: "hello.txt"
    shell: "echo Hello > {output}"
