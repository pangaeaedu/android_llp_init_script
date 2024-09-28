package build_src

object Versions {
    const val buildTools = "28.0.3"
    const val compileSdk = 28
    const val minSdk = 21
    const val targetSdk = 28

    const val support = "28.0.0"
    const val kotlin = "1.2.21"
}

object Libs {
    const val buildGradle = "com.android.tools.build:gradle:3.0.0"
    const val kotlinPlugin = "org.jetbrains.kotlin:kotlin-gradle-plugin:${Versions.kotlin}"
    const val kotlinStd = "org.jetbrains.kotlin:kotlin-stdlib-jdk7:${Versions.kotlin}"

    object Jackson {
        private const val version = "2.9.2"
        const val ann = "com.fasterxml.jackson.core:jackson-annotations:$version"
        const val core = "com.fasterxml.jackson.core:jackson-core:$version"
    }

    const val okHttp = "com.squareup.okhttp3:okhttp:3.12.1"

    object Kotlin {
        private const val corVersion = "1.2.2"
        const val coroutinesAndroid = "org.jetbrains.kotlinx:kotlinx-coroutines-android:$corVersion"
        const val coroutinesCore = "org.jetbrains.kotlinx:kotlinx-coroutines-core:$corVersion"
    }

    object Retrofit2 {
        const val version = "2.2.0"
        const val core = "com.squareup.retrofit2:retrofit:$version"
        const val converterJackson = "com.squareup.retrofit2:converter-jackson:2.1.0"
    }

    object AndroidX {
        private const val version = "1.0.0"
        const val appCompat = "androidx.appcompat:appcompat:${version}"
        const val fragment = "androidx.fragment:fragment:${version}"
        const val constraintLayout = "androidx.constraintlayout:constraintlayout:1.1.3"
        const val design = "com.google.android.material:material:${version}"
        const val recycleView = "androidx.recyclerview:recyclerview:${version}"
        const val ann = "androidx.annotation:annotation:${version}"

        private const val roomVersion = "2.2.6"
        const val roomCommon = "androidx.room:room-common:${roomVersion}"
        const val roomRuntime = "androidx.room:room-runtime:${roomVersion}"
        const val roomCompiler = "androidx.room:room-compiler:${roomVersion}"
        const val roomKtx = "androidx.room:room-ktx:${roomVersion}"

        private const val dataBindingVersion = "3.6.4"
        const val dataBindingRuntime = "androidx.databinding:databinding-runtime:${dataBindingVersion}"
    }

    // nd libs
    object Apf {
        const val full = "com.nd.android.smartcan:smartcan-appfactory:3.5.32-release.1"
        const val core = "com.nd.android.smartcan:smartcan-core-aar:3.4.03-release.1@aar"
        const val framework = "com.nd.android.smartcan:framework-aar:3.4.03-release.1@aar"
        const val mafImpl = "com.nd.sdp.android:maf-implement:3.1.3-release.1@aar"
        const val mafInf = "com.nd.sdp.android:maf-interface:3.1.2-release.1@aar"
        const val util = "com.nd.android.smartcan:commons-util-aar:3.4.03-release.1@aar"
        const val res = "com.nd.sdp.android.common:res:0.2.6-release@aar"
    }

    object Hmx {
        private const val version = "0.1-beta01"
        const val jpkLifecycle = "com.nd.xst.hermex:jpk-lifecycle:${version}"
        const val jpkView = "com.nd.xst.hermex:jpk-view:${version}"
    }

    object Xst{
        const val textLoader = "com.nd.sdp.android.xcloud:xcloud-textview-loader:1.0.6-rc01"
    }
}

