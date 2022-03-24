pipeline {
    agent {
        label 'docker'
    }
    options {
        timeout(time: 4, unit: 'HOURS')
    }
    // environment {
    // }
    stages {
        stage("Build Container") {
            steps {
                sh 'docker build -t python:latest -f Dockerfile .'
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'docker run --rm --user "$(id -u):$(id -g)" -i --rm -v /etc/passwd:/etc/passwd:ro -v "\$(pwd):/workspace" -w /workspace python:latest /bin/bash -c "PYTHONPATH=/workspace make test"'
            }
            post {
                always {
                    // pytest generates junit.xml-type artifacts, post these to jenkins
                    // set healthScaleFactor to zero to disable contribution of test result to build health 
                    // (i.e. we rely on the actual test runs failing)
                    junit testResults: 'pytest*.xml', allowEmptyResults: true, healthScaleFactor: 0.0
                }
            }
        }
        stage('Deliver') {
            agent {
                label 'docker'
                }
            environment {
//                VOLUME = '$PWD/sources:/src'
               VOLUME = '$(pwd)/src:/src'
//                IMAGE = 'cdrx/pyinstaller-linux:python3'
               IMAGE = 'cdrx/pyinstaller-windows:python3'

            }
            steps {
                    // for Linux
                    //sh 'docker run --rm -e PYTHONDONTWRITEBYTECODE=1 -v "\$(pwd):/src" ${IMAGE} "python3 -m PyInstaller -F ./src/pp_tracking_id.py"'

                    // for Windows
                    //sh 'docker run --rm -e PYTHONDONTWRITEBYTECODE=1 -v "\$(pwd):/src" ${IMAGE} "pyinstaller -F ./src/pp_tracking_id.py"'
                    // should work for Windows _and_ Linux
                    sh 'docker run  --rm -e PYTHONDONTWRITEBYTECODE=1 -v "\$(pwd):/src" ${IMAGE} "pyinstaller --onefile --noconsole ./src/pp_tracking_id.py"'

                }
            post {
                success {
                    // for Linux
                    //archiveArtifacts "dist/pp_tracking_id"
                    // for Windows
                    archiveArtifacts "dist/pp_tracking_id.exe"
                    sh 'docker run --rm -v "\$(pwd):/src" ${IMAGE} "rm -rf build dist && rm -rf *.spec"'
                }
            }
        }

    }
    post {
        cleanup {
            cleanWs()
        }
    }
}
