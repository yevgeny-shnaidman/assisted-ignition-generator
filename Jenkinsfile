pipeline {
  environment {
            GENERATOR_IMAGE = 'quay.io/ocpmetal/assisted-ignition-generator'
  }
  agent {
    node {
      label 'host'
    }

  }
  stages {
    stage('build') {
      steps {
        sh 'skipper make'
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

                    sh '''docker tag  ${GENERATOR_IMAGE} ${GENERATOR_IMAGE}:latest'''
                    sh '''docker tag  ${GENERATOR_IMAGE} ${GENERATOR_IMAGE}:${GIT_COMMIT}'''
                    sh '''docker push ${GENERATOR_IMAGE}:latest'''
                    sh '''docker push ${GENERATOR_IMAGE}:${GIT_COMMIT}'''
                }

     }
}
}