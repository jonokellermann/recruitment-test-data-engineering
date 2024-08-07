import PackageDescription

let package = Package(
    name: "example-swift",
    products: [
        .executable(name: "example-swift", targets: ["example-swift"]),
    ],
    dependencies: [
        .package(url: "https://github.com/Kitura/Swift-Kuery.git", from: "3.0.0"),
        .package(url: "https://github.com/Kitura/Swift-Kuery-MySQL.git", from: "3.0.0"),
    ],
    targets: [
        .target(
            name: "example-swift",
            dependencies: ["SwiftKuery", "SwiftKueryMySQL"]),
    ]
)