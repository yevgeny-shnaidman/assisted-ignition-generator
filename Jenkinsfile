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
}