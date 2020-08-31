pipeline {
  environment {
            GENERATOR = 'quay.io/ocpmetal/assisted-ignition-generator'
  }
  agent {
    node {
      label 'host'
    }

  }
  stages {
    stage('build') {
      steps {
        sh 'docker image prune -a -f'
        sh 'make build-image'
      }
    }


  stage('publish images on push to master') {
                when {
                    branch 'master'
                }

                steps {

                    withCredentials([usernamePassword(credentialsId: 'ocpmetal_cred', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                        sh '''docker login quay.io -u $USER -p $PASS'''
                    }

                    sh '''docker tag  ${GENERATOR} ${GENERATOR}:latest'''
                    sh '''docker tag  ${GENERATOR} ${GENERATOR}:${GIT_COMMIT}'''
                    sh '''docker push ${GENERATOR}:latest'''
                    sh '''docker push ${GENERATOR}:${GIT_COMMIT}'''
                }

     }
  }
  post {
    failure {
        script {
            if (env.BRANCH_NAME == 'master')
                stage('notify master branch fail') {
                    withCredentials([string(credentialsId: 'slack-token', variable: 'TOKEN')]) {
                        script {
                            def data = [text: "Attention! assisted-ignition-generator branch  test failed, see: ${BUILD_URL}"]
                            writeJSON(file: 'data.txt', json: data, pretty: 4)
                        }
                        sh '''curl -X POST -H 'Content-type: application/json' --data-binary "@data.txt"  https://hooks.slack.com/services/$TOKEN'''

                    }
                }
        }
    }
  }
}